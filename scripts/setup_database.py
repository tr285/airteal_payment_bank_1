#!/usr/bin/env python3
"""
Database setup script to initialize schema and seed data
Run this once to set up your database with admin and test users
"""

import sys
sys.path.insert(0, '/vercel/share/v0-project')

from models.database import db
from services.user_service import UserService
from werkzeug.security import generate_password_hash

def setup_database():
    print("[INFO] Initializing database schema...")
    
    # Schema is auto-initialized by the DatabaseAbstractionLayer constructor
    print("[INFO] Database schema initialized successfully!")
    
    # Seed initial data
    print("[INFO] Seeding initial data...")
    
    # Check if admin already exists
    admin = UserService.get_admin_user()
    if admin:
        print("[INFO] Admin user already exists, skipping seed data creation...")
        return
    
    try:
        # Create admin account
        admin_password = "admin123"
        hashed = generate_password_hash(admin_password)
        db.execute(
            "INSERT INTO users (full_name, mobile, password, balance, role) VALUES (%s, %s, %s, %s, %s)",
            ("Admin User", "9999999999", hashed, 50000.00, "admin")
        )
        print("✓ Admin account created!")
        print(f"  Mobile: 9999999999")
        print(f"  Password: {admin_password}")
        
        # Create test user 1
        user1_password = "user123"
        hashed1 = generate_password_hash(user1_password)
        db.execute(
            "INSERT INTO users (full_name, mobile, password, balance, role) VALUES (%s, %s, %s, %s, %s)",
            ("Raj Kumar", "9123456789", hashed1, 5000.00, "user")
        )
        print("✓ Test user 1 created!")
        print(f"  Mobile: 9123456789")
        print(f"  Password: {user1_password}")
        
        # Create test user 2
        user2_password = "user123"
        hashed2 = generate_password_hash(user2_password)
        db.execute(
            "INSERT INTO users (full_name, mobile, password, balance, role) VALUES (%s, %s, %s, %s, %s)",
            ("Priya Singh", "9198765432", hashed2, 3000.00, "user")
        )
        print("✓ Test user 2 created!")
        print(f"  Mobile: 9198765432")
        print(f"  Password: {user2_password}")
        
        print("\n[SUCCESS] Database setup completed!")
        print("\nYou can now login with:")
        print("  Admin: 9999999999 / admin123")
        print("  User1: 9123456789 / user123")
        print("  User2: 9198765432 / user123")
        
    except Exception as e:
        print(f"[ERROR] Failed to seed data: {e}")
        raise

if __name__ == "__main__":
    setup_database()
