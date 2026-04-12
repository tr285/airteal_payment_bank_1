#!/bin/bash

# Airtel Payment Bank - Startup Script

echo "================================"
echo "Airtel Payment Bank Setup"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from template..."
    cp .env.example .env 2>/dev/null || cat > .env << 'EOF'
SECRET_KEY=your_super_secret_key_change_in_production
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=airtel_payment_bank
MYSQL_PORT=3306
SUPABASE_DB_URL=
EOF
    echo "✓ .env file created"
    echo "  Please update .env with your database credentials"
    echo ""
fi

# Check Python version
python_version=$(python3 --version 2>&1)
echo "✓ Python $python_version"

# Check if venv exists
if [ ! -d venv ]; then
    echo ""
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate venv
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Initialize database
echo ""
echo "Initializing database..."
python scripts/setup_database.py

# Start application
echo ""
echo "================================"
echo "🚀 Starting Application..."
echo "================================"
echo ""
echo "📱 Visit: http://localhost:5000"
echo ""
echo "Test Credentials:"
echo "  Admin: 9999999999 / admin123"
echo "  User:  9123456789 / user123"
echo ""

python app.py
