from models.database import db
from services.user_service import UserService

class TransactionService:
    @staticmethod
    def get_user_transactions(user_id, limit=None):
        query = """
            SELECT t.id, t.amount, t.timestamp,
                   t.sender_id, t.receiver_id,
                   u1.full_name AS sender_name,
                   u2.full_name AS receiver_name
            FROM transactions t
            JOIN users u1 ON t.sender_id = u1.id
            JOIN users u2 ON t.receiver_id = u2.id
            WHERE t.sender_id=%s OR t.receiver_id=%s
            ORDER BY t.timestamp DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        return db.fetchall(query, (user_id, user_id))

    @staticmethod
    def get_all_transactions(limit=50):
        query = """
            SELECT t.id, t.amount, t.timestamp,
                   u1.full_name AS sender_name,
                   u2.full_name AS receiver_name
            FROM transactions t
            JOIN users u1 ON t.sender_id = u1.id
            JOIN users u2 ON t.receiver_id = u2.id
            ORDER BY t.timestamp DESC
            LIMIT %s
        """
        return db.fetchall(query, (limit,))
        
    @staticmethod
    def get_total_transactions_count():
        query = "SELECT COUNT(*) AS total_transactions FROM transactions"
        res = db.fetchone(query)
        return res["total_transactions"] if res else 0

    @staticmethod
    def transfer_money(sender_id, receiver_mobile, amount):
        if amount <= 0:
            return False, "Invalid amount"
            
        # Get Sender
        sender = UserService.get_user_by_id(sender_id)
        if not sender or sender['balance'] < amount:
            return False, "Insufficient balance"
            
        # Get Receiver
        query_recv = "SELECT id, full_name FROM users WHERE mobile=%s"
        receiver = db.fetchone(query_recv, (receiver_mobile,))
        if not receiver:
            return False, "Receiver not found"
            
        if sender_id == receiver['id']:
            return False, "Cannot send money to yourself"

        try:
            # We must use a transaction. The exact syntax for psycopg2 vs mysql can differ, but our execute method commits manually per statement.
            # To perform a true atomic operation, we could expand our DAL to support transactions properly.
            # For this simple DAL setup, we disable autocommit and do it.
            
            cursor = db._get_cursor()
            
            # Deduct from sender
            cursor.execute("UPDATE users SET balance = balance - %s WHERE id=%s", (amount, sender_id))
            # Add to receiver
            cursor.execute("UPDATE users SET balance = balance + %s WHERE id=%s", (amount, receiver['id']))
            # Insert record
            cursor.execute("""
                INSERT INTO transactions (sender_id, receiver_id, amount)
                VALUES (%s, %s, %s)
            """, (sender_id, receiver['id'], amount))
            
            db.commit()
            return True, receiver['full_name']
            
        except Exception as e:
            db.rollback()
            return False, str(e)
            
    @staticmethod
    def deposit_money(user_id, amount):
        if amount <= 0:
            return False, "Invalid Amount"
            
        admin = UserService.get_admin_user()
        if not admin:
            return False, "Admin account not found for simulation"
            
        admin_id = admin["id"]
        
        if user_id == admin_id:
            return False, "Admin cannot deposit using this method"

        try:
            cursor = db._get_cursor()
            
            # In real banking: add money from external source (bank transfers, ATM deposits, etc.)
            # We simulate this by only adding to the user account (no deduction from admin)
            # This represents money coming into the banking system
            cursor.execute("UPDATE users SET balance = balance + %s WHERE id=%s", (amount, user_id))
            
            # Insert record with admin as sender to track deposits
            cursor.execute("""
                INSERT INTO transactions (sender_id, receiver_id, amount)
                VALUES (%s, %s, %s)
            """, (admin_id, user_id, amount))
            
            db.commit()
            return True, "Deposit successful"
            
        except Exception as e:
            db.rollback()
            return False, str(e)

    @staticmethod
    def delete_transaction(transaction_id):
        query = "DELETE FROM transactions WHERE id=%s"
        db.execute(query, (transaction_id,))
