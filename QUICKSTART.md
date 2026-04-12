# Airtel Payment Bank - Quick Start Guide

This guide will help you get the Airtel Payment Bank application running in minutes.

## Prerequisites

- Python 3.8 or higher
- MySQL 5.7+ OR PostgreSQL 12+ (or Supabase)
- pip (Python package manager)

## Step 1: Clone and Setup

```bash
# Navigate to project directory
cd airteal_payment_bank_1

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Database Configuration

### Option A: MySQL (Recommended)

1. **Create database:**
   ```bash
   mysql -u root -p
   CREATE DATABASE airtel_payment_bank;
   ```

2. **Create .env file** in the project root:
   ```
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=airtel_payment_bank
   MYSQL_PORT=3306
   SECRET_KEY=your_secret_key_here
   ```

3. **Initialize database schema:**
   ```bash
   mysql -u root -p airtel_payment_bank < database/schema.sql
   mysql -u root -p airtel_payment_bank < database/seed_data.sql
   ```

### Option B: Supabase (PostgreSQL Cloud)

1. **Create a Supabase account** at https://supabase.com

2. **Create .env file** with:
   ```
   SUPABASE_DB_URL=postgresql://user:password@host:5432/postgres
   SECRET_KEY=your_secret_key_here
   ```

3. **Run the schema** in Supabase SQL editor:
   - Copy content from `database/schema.sql`
   - Adjust SQL syntax for PostgreSQL (use SERIAL instead of AUTO_INCREMENT)

## Step 3: Run the Application

```bash
# Start the Flask server
python app.py

# Or use the startup script
# On macOS/Linux:
chmod +x start.sh
./start.sh

# On Windows:
start.bat
```

The application will be available at: **http://localhost:5000**

## Step 4: Login

Use these test credentials:

### Admin Account
- **Mobile:** 9999999999
- **Password:** admin123

### Test User 1
- **Mobile:** 9123456789
- **Password:** user123

### Test User 2
- **Mobile:** 9198765432
- **Password:** user123

## Features Available

✓ User Registration
✓ Login/Logout
✓ Money Transfer
✓ Deposit/Withdrawal
✓ Transaction History
✓ Admin Dashboard
✓ User Management
✓ Real-time Balance Updates

## Troubleshooting

### MySQL Connection Error
**Problem:** `OperationalError: (2003, "Can't connect to MySQL server")`

**Solution:**
1. Ensure MySQL is running: `mysql -u root -p -e "SELECT 1"`
2. Check credentials in `.env` file
3. Verify database exists: `CREATE DATABASE airtel_payment_bank;`

### Module Not Found Error
**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Port Already in Use
**Problem:** `Address already in use on port 5000`

**Solution:**
- Change port in `app.py`: `app.run(port=5001)`
- Or kill process: `lsof -ti:5000 | xargs kill -9` (macOS/Linux)

### Supabase Connection Issue
**Problem:** PostgreSQL connection timeout

**Solution:**
1. Verify SUPABASE_DB_URL format is correct
2. Check your Supabase database is active
3. Ensure IP address is whitelisted in Supabase

## Project Structure

```
airteal_payment_bank_1/
├── app.py                    # Main Flask application
├── config/
│   └── settings.py          # Configuration settings
├── models/
│   └── database.py          # Database abstraction layer
├── services/
│   ├── user_service.py      # User business logic
│   └── transaction_service.py # Transaction logic
├── routes/
│   ├── auth.py              # Login/Register routes
│   ├── user.py              # User routes
│   ├── transaction.py       # Transaction routes
│   ├── admin.py             # Admin dashboard routes
│   └── api.py               # API endpoints
├── templates/               # HTML templates
├── static/                  # CSS, JavaScript, images
└── database/
    ├── schema.sql           # Database schema
    └── seed_data.sql        # Initial test data
```

## API Endpoints

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference.

### Key Endpoints:
- `POST /login` - User login
- `POST /register` - User registration
- `GET /dashboard` - User dashboard
- `POST /transfer` - Send money
- `POST /deposit` - Deposit money
- `GET /transactions` - View history
- `GET /admin` - Admin panel

## Next Steps

1. Customize the application (branding, features, etc.)
2. Add more users and transactions
3. Deploy to a production server
4. Set up email notifications
5. Add two-factor authentication

## Support

For issues or questions, refer to:
- [INSTALLATION.md](INSTALLATION.md) - Detailed setup guide
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Code organization

Happy Banking! 🏦
