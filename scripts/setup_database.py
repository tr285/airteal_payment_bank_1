#!/usr/bin/env python3
"""
Database setup script to initialize schema and seed data
Run this once to set up your database with admin and test users
"""

import os
import sys
import mysql.connector
import psycopg2
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_connection():
    """Get database connection with fallback support"""
    # Try MySQL first
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DATABASE', 'airtel_payment_bank'),
            port=int(os.getenv('MYSQL_PORT', 3306))
        )
        if conn.is_connected():
            print("[INFO] Connected to MySQL database")
            return conn, 'mysql'
    except Exception as e:
        print(f"[WARNING] MySQL connection failed: {e}")
    
    # Fallback to PostgreSQL/Supabase
    try:
        db_url = os.getenv('SUPABASE_DB_URL')
        if db_url:
            conn = psycopg2.connect(db_url)
            print("[INFO] Connected to PostgreSQL/Supabase database")
            return conn, 'postgres'
    except Exception as e:
        print(f"[WARNING] PostgreSQL connection failed: {e}")
    
    print("[ERROR] No database connection available!")
    sys.exit(1)

def init_schema(cursor, db_type):
    """Initialize database schema"""
    if db_type == 'mysql':
        schema_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            mobile VARCHAR(20) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            balance DECIMAL(15, 2) DEFAULT 0.00,
            role ENUM('user', 'admin') DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender_id INT NOT NULL,
            receiver_id INT NOT NULL,
            amount DECIMAL(15, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS audit_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            action VARCHAR(255),
            details JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
        for statement in schema_sql.split(';'):
            if statement.strip():
                cursor.execute(statement)
    else:  # PostgreSQL
        schema_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            mobile VARCHAR(20) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            balance DECIMAL(15, 2) DEFAULT 0.00,
            role VARCHAR(20) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            sender_id INT NOT NULL,
            receiver_id INT NOT NULL,
            amount DECIMAL(15, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS audit_logs (
            id SERIAL PRIMARY KEY,
            user_id INT,
            action VARCHAR(255),
            details JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
        cursor.execute(schema_sql)

def seed_data(cursor, conn, db_type):
    """Seed initial test data"""
    try:
        # Check if admin already exists
        cursor.execute("SELECT * FROM users WHERE role = %s", ('admin',))
        if cursor.fetchone():
            print("[INFO] Admin user already exists, skipping seed data...")
            return
        
        # Create admin account
        admin_password = "admin123"
        hashed = generate_password_hash(admin_password)
        cursor.execute(
            "INSERT INTO users (full_name, mobile, password, balance, role) VALUES (%s, %s, %s, %s, %s)",
            ("Admin User", "9999999999", hashed, 50000.00, "admin")
        )
        print("✓ Admin account created!")
        print(f"  Mobile: 9999999999")
        print(f"  Password: {admin_password}")
        
        # Create test user 1
        user1_password = "user123"
        hashed1 = generate_password_hash(user1_password)
        cursor.execute(
            "INSERT INTO users (full_name, mobile, password, balance, role) VALUES (%s, %s, %s, %s, %s)",
            ("Raj Kumar", "9123456789", hashed1, 5000.00, "user")
        )
        print("✓ Test user 1 created!")
        print(f"  Mobile: 9123456789")
        print(f"  Password: {user1_password}")
        
        # Create test user 2
        user2_password = "user123"
        hashed2 = generate_password_hash(user2_password)
        cursor.execute(
            "INSERT INTO users (full_name, mobile, password, balance, role) VALUES (%s, %s, %s, %s, %s)",
            ("Priya Singh", "9198765432", hashed2, 3000.00, "user")
        )
        print("✓ Test user 2 created!")
        print(f"  Mobile: 9198765432")
        print(f"  Password: {user2_password}")
        
        conn.commit()
        
        print("\n[SUCCESS] Database setup completed!")
        print("\nYou can now login with:")
        print("  Admin: 9999999999 / admin123")
        print("  User1: 9123456789 / user123")
        print("  User2: 9198765432 / user123")
        
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to seed data: {e}")
        raise

def setup_database():
    """Main setup function"""
    print("[INFO] Initializing database schema...")
    
    conn, db_type = get_connection()
    
    try:
        if db_type == 'mysql':
            cursor = conn.cursor()
        else:
            cursor = conn.cursor()
        
        init_schema(cursor, db_type)
        conn.commit()
        print("[INFO] Database schema initialized successfully!")
        
        print("[INFO] Seeding initial data...")
        seed_data(cursor, conn, db_type)
        
        cursor.close()
        
    finally:
        if conn.is_connected():
            conn.close()

if __name__ == "__main__":
    setup_database()
