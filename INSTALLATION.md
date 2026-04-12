# Complete Installation Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Local Setup](#local-setup)
3. [Database Setup](#database-setup)
4. [Running the Application](#running-the-application)
5. [Docker Setup](#docker-setup)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **Memory**: 512MB RAM
- **Disk Space**: 500MB
- **Database**: MySQL 5.7+ OR PostgreSQL 12+ (via Supabase)

### Recommended
- Python 3.10+
- 2GB+ RAM
- Modern browser (Chrome, Firefox, Safari, Edge)

---

## Local Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/airtel_payment_bank.git
cd airtel_payment_bank
```

### 2. Create Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy template to .env
cp .env.example .env

# Edit .env with your database credentials
nano .env  # or use your favorite editor
```

---

## Database Setup

### Option A: MySQL (Local)

**Install MySQL:**

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

**Mac (Homebrew):**
```bash
brew install mysql
mysql.server start
mysql_secure_installation
```

**Windows:**
- Download from: https://dev.mysql.com/downloads/mysql/
- Run installer and follow wizard
- Remember the root password you set

**Verify Installation:**
```bash
mysql -u root -p
# Type your password and verify connection works
# Type 'exit' to quit
```

**Configure .env:**
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=airtel_payment_bank
MYSQL_PORT=3306
```

---

### Option B: Supabase (Cloud PostgreSQL)

**Sign Up:**
1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up with email or GitHub

**Create Project:**
1. Create new project
2. Choose region (closest to you)
3. Set strong password
4. Wait for project to be ready (~2 minutes)

**Get Connection String:**
1. In Supabase dashboard, click "Connect"
2. Select "Python" from dropdown
3. Copy the connection string
4. Keep the password you set

**Configure .env:**
```env
SUPABASE_DB_URL=postgresql://postgres:YOUR_PASSWORD@YOUR_HOST:5432/postgres
MYSQL_HOST=localhost
MYSQL_USER=root
```

**Test Connection:**
```bash
python -c "from models.database import db; print('✓ Database connected!')"
```

---

## Running the Application

### Quick Start (Automated)

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
start.bat
```

This will:
- Create virtual environment
- Install dependencies
- Initialize database with test data
- Start the application

### Manual Setup

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Initialize database
python scripts/setup_database.py

# Start Flask application
python app.py
```

### Access Application
```
Open browser: http://localhost:5000
```

### Test Credentials
After setup, use these to login:

| Type | Mobile | Password |
|------|--------|----------|
| Admin | 9999999999 | admin123 |
| User | 9123456789 | user123 |
| User | 9198765432 | user123 |

---

## Docker Setup

### Prerequisites
- Docker installed: https://www.docker.com/products/docker-desktop

### Build Image
```bash
docker build -t airtel-payment-bank:latest .
```

### Run with Docker Compose (Recommended)

**Create `docker-compose.override.yml`:**
```yaml
version: '3.8'

services:
  app:
    environment:
      - MYSQL_HOST=mysql
      - MYSQL_USER=root
      - MYSQL_PASSWORD=rootpassword
      - MYSQL_DATABASE=airtel_payment_bank
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: airtel_payment_bank
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

**Run:**
```bash
docker-compose up --build
```

### Run Standalone
```bash
docker run -p 5000:5000 \
  -e MYSQL_HOST=host.docker.internal \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=yourpassword \
  -e MYSQL_DATABASE=airtel_payment_bank \
  airtel-payment-bank:latest
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
pip install -r requirements.txt
```

### "Can't connect to MySQL server"
**Check:**
1. MySQL is running: `mysql -u root -p`
2. Credentials in .env are correct
3. Database exists: `CREATE DATABASE airtel_payment_bank;`

**Fix:**
```bash
# Create database if missing
mysql -u root -p -e "CREATE DATABASE airtel_payment_bank;"

# Run setup script
python scripts/setup_database.py
```

### "Connection refused" for Supabase
**Check:**
1. SUPABASE_DB_URL is correct in .env
2. Connection string includes password
3. Project is active in Supabase dashboard

**Test:**
```bash
psql "postgresql://user:password@host/database"
```

### Admin user not created
**Fix:**
```bash
# Re-run setup
python scripts/setup_database.py

# Check users
mysql -u root -p airtel_payment_bank -e "SELECT * FROM users;"
```

### "Port 5000 already in use"
**Solution 1 - Use different port:**
```bash
python app.py --port 5001
```

**Solution 2 - Kill process on port 5000:**

Linux/Mac:
```bash
lsof -i :5000
kill -9 <PID>
```

Windows:
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Database tables not created
**Fix:**
```bash
# Delete .env and recreate
rm .env
cp .env.example .env

# Update .env with correct credentials

# Run setup
python scripts/setup_database.py
```

### "CSRF token missing" on forms
- Clear browser cookies
- Restart application
- Check SECRET_KEY in .env is not empty

---

## Advanced Configuration

### Environment Variables
See `.env.example` for all available options.

### Production Setup
1. Change `SECRET_KEY` to secure random value
2. Set `FLASK_ENV=production`
3. Use gunicorn instead of Flask dev server:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
4. Use nginx as reverse proxy
5. Enable HTTPS/SSL certificates

### Logging
Logs are printed to console. To save to file:
```bash
python app.py > app.log 2>&1 &
```

---

## Getting Help

### Health Check
```bash
curl http://localhost:5000/health
```

### Common Paths
- Admin Dashboard: http://localhost:5000/admin
- User Dashboard: http://localhost:5000/dashboard
- API Docs: http://localhost:5000/api/live-transactions

### Support
- GitHub Issues: Create issue in repository
- Email: support@example.com
- Documentation: See SETUP.md
