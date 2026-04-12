# Airtel Payment Bank - Setup & Deployment Guide

## Quick Start (Local Development)

### Prerequisites
- Python 3.8+
- MySQL Server running locally, OR Supabase account for PostgreSQL

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Database
Edit `.env` file with your database credentials:

**For MySQL (Local):**
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=airtel_payment_bank
MYSQL_PORT=3306
```

**For Supabase (Cloud PostgreSQL):**
```env
SUPABASE_DB_URL=postgresql://user:password@host:port/database
MYSQL_HOST=localhost  # Keep for fallback
MYSQL_USER=root
MYSQL_PASSWORD=
```

### Step 3: Initialize Database & Seed Data
```bash
python scripts/setup_database.py
```

This creates:
- Database tables
- Admin account (9999999999 / admin123)
- Test users (9123456789, 9198765432 with password user123)

### Step 4: Run Application
```bash
python app.py
```

Visit: `http://localhost:5000`

---

## Docker Deployment

### Build Image
```bash
docker build -t airtel-payment-bank .
```

### Run Container
```bash
docker run -p 5000:5000 \
  -e MYSQL_HOST=mysql-host \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=yourpass \
  -e MYSQL_DATABASE=airtel_payment_bank \
  airtel-payment-bank
```

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `SECRET_KEY` | Flask session key | fallback_secret_key |
| `MYSQL_HOST` | MySQL server address | localhost |
| `MYSQL_USER` | MySQL username | root |
| `MYSQL_PASSWORD` | MySQL password | (empty) |
| `MYSQL_DATABASE` | Database name | airtel_payment_bank |
| `MYSQL_PORT` | MySQL port | 3306 |
| `SUPABASE_DB_URL` | Supabase connection string | (empty) |

---

## Database Support

### Primary Database: MySQL
- Used by default if available
- Auto-initializes schema on first run

### Fallback Database: Supabase (PostgreSQL)
- Automatically used if MySQL unavailable
- Requires `SUPABASE_DB_URL` in `.env`
- Perfect for cloud deployments

---

## Test Credentials

After running `setup_database.py`, use these to test:

| Role | Mobile | Password |
|------|--------|----------|
| Admin | 9999999999 | admin123 |
| User | 9123456789 | user123 |
| User | 9198765432 | user123 |

---

## Features Included

✅ User Registration & Login  
✅ Money Transfers  
✅ Deposits (QR/UPI simulation)  
✅ Transaction History  
✅ PDF Statement Downloads  
✅ Profile Management  
✅ Admin Dashboard  
✅ Responsive Mobile UI  

---

## Troubleshooting

### "Database connection failed"
- Check MySQL is running: `mysql -u root -p`
- Or set `SUPABASE_DB_URL` for PostgreSQL fallback

### "Mobile number already exists"
- Register with a different phone number
- Or delete the user from database: `DELETE FROM users WHERE mobile='9123456789';`

### Admin features not showing
- Verify you're logged in as admin (role='admin')
- Create admin user: Update `.env` and run `setup_database.py`

---

## Next Steps for Production

1. **Enhance Security**
   - Change `SECRET_KEY` in `.env`
   - Use HTTPS/TLS
   - Add rate limiting
   - Implement CSRF protection

2. **Real Payment Gateway**
   - Integrate Razorpay or Stripe
   - Replace UPI simulation with real gateway

3. **OTP Verification**
   - Add Twilio/AWS SNS for SMS OTP
   - Verify phone during registration

4. **Monitoring & Logging**
   - Set up logging to files
   - Monitor database connections
   - Track user activity

5. **Cloud Deployment**
   - Deploy to Render.com, Railway, or Heroku
   - Use managed PostgreSQL (Supabase, Neon, AWS RDS)
   - Set up CI/CD pipeline
