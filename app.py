from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
import random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes

app = Flask(__name__)
app.secret_key = "supersecretkey"

cursor = db.cursor(dictionary=True)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"]
        mobile = request.form["mobile"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (full_name, mobile, password) VALUES (%s, %s, %s)",
            (full_name, mobile, hashed_password)
        )
        db.commit()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mobile = request.form["mobile"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE mobile=%s", (mobile,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]

            flash("Login Successful 💙", "success")
            return redirect("/dashboard")
        else:
            flash("Invalid Mobile or Password ❌", "danger")
            return redirect("/login")

    return render_template("login.html")

# ---------------- VERIFY OTP ----------------


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    cursor.execute("SELECT full_name, balance, role FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    cursor.execute("""
        SELECT t.amount, t.timestamp,
               t.sender_id, t.receiver_id,
               u1.full_name AS sender_name,
               u2.full_name AS receiver_name
        FROM transactions t
        JOIN users u1 ON t.sender_id = u1.id
        JOIN users u2 ON t.receiver_id = u2.id
        WHERE t.sender_id=%s OR t.receiver_id=%s
        ORDER BY t.timestamp DESC
    """, (user_id, user_id))

    transactions = cursor.fetchall()

    total_deposit = 0
    total_sent = 0

    for t in transactions:
        if t["sender_id"] == user_id and t["receiver_id"] == user_id:
            total_deposit += float(t["amount"])
        elif t["sender_id"] == user_id:
            total_sent += float(t["amount"])

    total_transactions = len(transactions)

    return render_template(
        "dashboard.html",
        name=user["full_name"],
        balance=user["balance"],
        role=user["role"],
        transactions=transactions[:5],
        total_deposit=total_deposit,
        total_sent=total_sent,
        total_transactions=total_transactions
    )
# ---------------- TRANSFER ----------------
@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if "user_id" not in session:
        return redirect("/login")

    sender_id = session["user_id"]

    cursor.execute("SELECT balance FROM users WHERE id=%s", (sender_id,))
    sender = cursor.fetchone()

    if request.method == "POST":
        receiver_mobile = request.form["receiver_mobile"]
        amount = float(request.form["amount"])

        cursor.execute("SELECT id, full_name FROM users WHERE mobile=%s", (receiver_mobile,))
        receiver = cursor.fetchone()

        if not receiver:
            flash("Receiver not found ❌", "danger")
            return redirect("/transfer")

        if sender["balance"] < amount:
            flash("Insufficient balance ❌", "danger")
            return redirect("/transfer")

        receiver_id = receiver["id"]

        cursor.execute(
            "UPDATE users SET balance = balance - %s WHERE id=%s",
            (amount, sender_id)
        )

        cursor.execute(
            "UPDATE users SET balance = balance + %s WHERE id=%s",
            (amount, receiver_id)
        )

        cursor.execute("""
            INSERT INTO transactions (sender_id, receiver_id, amount)
            VALUES (%s, %s, %s)
        """, (sender_id, receiver_id, amount))

        db.commit()

        return render_template(
            "transfer_success.html",
            amount=amount,
            receiver_name=receiver["full_name"]
        )

    return render_template("transfer.html", balance=sender["balance"])


    # ---------------------admin -delete history section---------------------
@app.route("/delete-transaction/<int:transaction_id>")
def delete_transaction(transaction_id):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    cursor.execute("SELECT role FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if user["role"] != "admin":
        return "Access Denied ❌"

    cursor.execute("DELETE FROM transactions WHERE id=%s", (transaction_id,))
    db.commit()

    flash("Transaction Deleted Successfully 🗑", "success")
    return redirect("/admin")




    # ---------------- TRANSACTION HISTORY ----------------
@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    cursor.execute("""
        SELECT t.amount, t.timestamp,
               t.sender_id, t.receiver_id,
               u1.full_name AS sender_name,
               u2.full_name AS receiver_name
        FROM transactions t
        JOIN users u1 ON t.sender_id = u1.id
        JOIN users u2 ON t.receiver_id = u2.id
        WHERE t.sender_id=%s OR t.receiver_id=%s
        ORDER BY t.timestamp DESC
    """, (user_id, user_id))

    transactions = cursor.fetchall()

    return render_template("history.html",
                           transactions=transactions,
                           user_id=user_id)



# ---------------- DEPOSIT ----------------
from datetime import datetime
import uuid

@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        user_id = session["user_id"]
        amount = float(request.form["amount"])

        if amount <= 0:
            return "Invalid Amount ❌"

        # 🔹 Get Admin ID
        cursor.execute("SELECT id FROM users WHERE role='admin'")
        admin = cursor.fetchone()

        if not admin:
            return "Admin account not found ❌"

        admin_id = admin["id"]

        # 🔹 Increase ADMIN balance (money received)
        cursor.execute(
            "UPDATE users SET balance = balance + %s WHERE id=%s",
            (amount, admin_id)
        )

        # 🔹 Increase USER balance (wallet credited)
        cursor.execute(
            "UPDATE users SET balance = balance + %s WHERE id=%s",
            (amount, user_id)
        )

        # 🔹 Record transaction (admin → user)
        cursor.execute("""
            INSERT INTO transactions (sender_id, receiver_id, amount)
            VALUES (%s, %s, %s)
        """, (admin_id, user_id, amount))

        db.commit()

        transaction_id = str(uuid.uuid4())[:8].upper()
        payment_time = datetime.now().strftime("%d %b %Y, %I:%M %p")

        return render_template(
            "receipt.html",
            transaction_id=transaction_id,
            amount=amount,
            payment_time=payment_time,
            upi_id="adminbank@upi"
        )

    return render_template("deposit.html")

# ---------------- ADMIN ----------------
@app.route("/admin")
def admin_panel():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    cursor.execute("SELECT role FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if user["role"] != "admin":
        return "Access Denied ❌"

    # Total Users
    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    total_users = cursor.fetchone()["total_users"]

    # Total Transactions
    cursor.execute("SELECT COUNT(*) AS total_transactions FROM transactions")
    total_transactions = cursor.fetchone()["total_transactions"]

    # Total Bank Balance
    cursor.execute("SELECT SUM(balance) AS total_balance FROM users")
    total_balance = cursor.fetchone()["total_balance"] or 0

    # Users List
    cursor.execute("SELECT id, full_name, mobile, balance, role FROM users")
    users = cursor.fetchall()

    # Transactions List
    cursor.execute("""
        SELECT t.amount, t.timestamp,
               u1.full_name AS sender_name,
               u2.full_name AS receiver_name
        FROM transactions t
        JOIN users u1 ON t.sender_id = u1.id
        JOIN users u2 ON t.receiver_id = u2.id
        ORDER BY t.timestamp DESC
    """)
    transactions = cursor.fetchall()

    return render_template("admin.html",
                           total_users=total_users,
                           total_transactions=total_transactions,
                           total_balance=total_balance,
                           users=users,
                           transactions=transactions)


# ------------------------profile section-----------------------------------

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # Get user data
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if request.method == "POST":

        # Update Name
        if "update_profile" in request.form:
            full_name = request.form["full_name"]
            cursor.execute("UPDATE users SET full_name=%s WHERE id=%s",
                           (full_name, user_id))
            db.commit()
            flash("Profile Updated Successfully 💙", "success")
            return redirect("/profile")

        # Change Password
        if "change_password" in request.form:
            current_password = request.form["current_password"]
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]

            # Check current password
            if not check_password_hash(user["password"], current_password):
                flash("Current password is incorrect ❌", "danger")
                return redirect("/profile")

            if new_password != confirm_password:
                flash("New passwords do not match ❌", "danger")
                return redirect("/profile")

            hashed_password = generate_password_hash(new_password)

            cursor.execute("UPDATE users SET password=%s WHERE id=%s",
                           (hashed_password, user_id))
            db.commit()

            flash("Password Changed Successfully 🔐", "success")
            return redirect("/profile")

    return render_template("profile.html", user=user)

    #----------download statement -section
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.platypus import TableStyle
import io
from flask import send_file
from datetime import datetime


@app.route("/download-statement")
def download_statement():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # Get user info
    cursor.execute("SELECT full_name FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    # Get transactions
    cursor.execute("""
        SELECT t.amount, t.timestamp,
               u1.full_name AS sender_name,
               u2.full_name AS receiver_name
        FROM transactions t
        JOIN users u1 ON t.sender_id = u1.id
        JOIN users u2 ON t.receiver_id = u2.id
        WHERE t.sender_id=%s OR t.receiver_id=%s
        ORDER BY t.timestamp DESC
    """, (user_id, user_id))

    transactions = cursor.fetchall()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
    elements = []

    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("<b>Airtel Payments Bank</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Account Holder: {user['full_name']}", styles["Normal"]))
    elements.append(Paragraph(f"Generated On: {datetime.now().strftime('%d %b %Y %I:%M %p')}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Table Data
    data = [["Sender", "Receiver", "Amount (₹)", "Date"]]

    for t in transactions:
        data.append([
            t["sender_name"],
            t["receiver_name"],
            str(t["amount"]),
            str(t["timestamp"])
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.red),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey)
    ]))

    elements.append(table)

    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="statement.pdf",
        mimetype="application/pdf"
    )



# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# 🔥 MUST BE LAST
if __name__ == "__main__":
    app.run(debug=True)