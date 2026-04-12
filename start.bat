@echo off
REM Airtel Payment Bank - Windows Startup Script

echo.
echo ================================
echo Airtel Payment Bank Setup
echo ================================
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env file...
    (
        echo SECRET_KEY=your_super_secret_key_change_in_production
        echo MYSQL_HOST=localhost
        echo MYSQL_USER=root
        echo MYSQL_PASSWORD=
        echo MYSQL_DATABASE=airtel_payment_bank
        echo MYSQL_PORT=3306
        echo SUPABASE_DB_URL=
    ) > .env
    echo .env file created. Please update with your database credentials.
    echo.
)

REM Check if venv exists
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
    echo Virtual environment created.
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -q -r requirements.txt
echo Dependencies installed.

REM Initialize database
echo.
echo Initializing database...
python scripts/setup_database.py

REM Start application
echo.
echo ================================
echo Starting Application...
echo ================================
echo.
echo Visit: http://localhost:5000
echo.
echo Test Credentials:
echo   Admin: 9999999999 / admin123
echo   User:  9123456789 / user123
echo.

python app.py
pause
