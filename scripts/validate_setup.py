#!/usr/bin/env python3
"""
Validation script to check if the application is properly configured
Run this before starting the application to verify everything is set up correctly
"""

import sys
import os
sys.path.insert(0, '/vercel/share/v0-project')

def check_python_version():
    """Check Python version is 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✓ Python {version.major}.{version.minor}")
    return True

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('/vercel/share/v0-project/.env'):
        print("❌ .env file not found")
        print("   Create it by copying: cp .env.example .env")
        return False
    print("✓ .env file found")
    return True

def check_requirements():
    """Check if all packages are installed"""
    required = ['flask', 'mysql', 'psycopg2', 'werkzeug', 'reportlab', 'python-dotenv']
    missing = []
    
    for pkg in required:
        try:
            if pkg == 'mysql':
                __import__('mysql.connector')
            elif pkg == 'psycopg2':
                __import__('psycopg2')
            else:
                __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    print("✓ All required packages installed")
    return True

def check_database():
    """Check database connectivity"""
    try:
        from models.database import db
        # Try a simple query
        result = db.fetchone("SELECT 1")
        if result:
            db_type = db._active_db
            print(f"✓ Database connected ({db_type})")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Check your .env file and ensure database is running")
        return False

def check_tables():
    """Check if database tables exist"""
    try:
        from models.database import db
        
        # Check users table
        result = db.fetchone("SELECT COUNT(*) as count FROM users")
        if result is None:
            print("❌ Tables not created")
            print("   Run: python scripts/setup_database.py")
            return False
            
        user_count = result.get('count') if isinstance(result, dict) else result[0]
        print(f"✓ Database tables exist ({user_count} users)")
        return True
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def check_static_files():
    """Check if static files exist"""
    static_dir = '/vercel/share/v0-project/static'
    templates_dir = '/vercel/share/v0-project/templates'
    
    if not os.path.exists(static_dir):
        print("❌ static directory not found")
        return False
    
    if not os.path.exists(templates_dir):
        print("❌ templates directory not found")
        return False
        
    if not os.path.exists(f'{static_dir}/css/style.css'):
        print("⚠️  CSS file not found")
    
    print("✓ Static files and templates exist")
    return True

def check_secret_key():
    """Check if SECRET_KEY is set"""
    from config.settings import settings
    
    if settings.SECRET_KEY == "fallback_secret_key":
        print("⚠️  Using default SECRET_KEY (change in .env for production)")
        return True
    
    if not settings.SECRET_KEY or settings.SECRET_KEY.startswith("your_"):
        print("❌ SECRET_KEY not properly configured")
        return False
    
    print("✓ SECRET_KEY is configured")
    return True

def main():
    print("\n" + "="*50)
    print("Airtel Payment Bank - Setup Validation")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("Required Packages", check_requirements),
        ("Secret Key", check_secret_key),
        ("Database Connection", check_database),
        ("Database Tables", check_tables),
        ("Static Files", check_static_files),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        try:
            results.append(check_func())
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"✓ All checks passed ({passed}/{total})")
        print("\n🚀 Ready to start: python app.py")
        print("="*50 + "\n")
        return 0
    else:
        print(f"❌ Some checks failed ({passed}/{total})")
        print("\n⚠️  Please fix the issues above and try again")
        print("="*50 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
