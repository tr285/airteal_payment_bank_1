# Project Structure & Architecture

## Directory Overview

```
airtel_payment_bank/
│
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── package.json                    # Node.js dependencies (frontend tools)
├── Dockerfile                      # Docker container configuration
├── docker-compose.yml              # Docker orchestration
├── start.sh                        # Linux/Mac startup script
├── start.bat                       # Windows startup script
│
├── .env                            # Environment variables (create from .env.example)
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
│
├── config/                         # Configuration module
│   ├── __init__.py
│   └── settings.py                # Settings loader from environment
│
├── models/                         # Database models
│   ├── __init__.py
│   └── database.py                # Database abstraction layer (MySQL + PostgreSQL)
│
├── services/                       # Business logic services
│   ├── __init__.py
│   ├── user_service.py            # User operations (CRUD, auth, profile)
│   └── transaction_service.py     # Transaction operations (transfer, deposit, history)
│
├── routes/                         # API routes (blueprints)
│   ├── __init__.py
│   ├── auth.py                    # Authentication routes (register, login, logout)
│   ├── user.py                    # User routes (dashboard, profile, history)
│   ├── transaction.py             # Transaction routes (transfer, deposit, statement)
│   ├── admin.py                   # Admin routes (admin panel, management)
│   └── api.py                     # REST API endpoints
│
├── templates/                      # HTML templates (Jinja2)
│   ├── base.html                  # Base template with layout
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── dashboard.html             # User dashboard
│   ├── profile.html               # User profile page
│   ├── history.html               # Transaction history
│   ├── transfer.html              # Money transfer form
│   ├── transfer_success.html      # Transfer confirmation
│   ├── deposit.html               # Deposit form
│   ├── receipt.html               # Deposit receipt
│   ├── verify_otp.html            # OTP verification (placeholder)
│   ├── admin.html                 # Admin dashboard
│   ├── 404.html                   # 404 error page
│   └── 500.html                   # 500 error page
│
├── static/                        # Static assets
│   ├── css/
│   │   └── style.css              # Main stylesheet
│   ├── js/
│   │   └── app.js                 # Frontend JavaScript
│   └── images/
│       └── myupi.jpg              # UPI QR image
│
├── scripts/                       # Utility scripts
│   ├── setup_database.py          # Database initialization & seeding
│   └── validate_setup.py          # Setup validation checker
│
├── database/
│   └── schema.sql                 # SQL schema (reference)
│
└── Documentation/
    ├── README.md                  # Project overview
    ├── SETUP.md                   # Quick setup guide
    ├── INSTALLATION.md            # Detailed installation
    ├── API_DOCUMENTATION.md       # API reference
    └── PROJECT_STRUCTURE.md       # This file
```

---

## Architecture

### Technology Stack

**Backend:**
- Framework: Flask 3.0.0 (Python)
- Database: MySQL 5.7+ (primary) or PostgreSQL via Supabase (fallback)
- Web Server: Gunicorn (production) or Flask dev server (development)
- ORM: Custom DatabaseAbstractionLayer (handles MySQL & PostgreSQL)
- Authentication: Session-based (Flask sessions)
- Password Hashing: Werkzeug security
- PDF Generation: ReportLab

**Frontend:**
- Markup: HTML5
- Styling: CSS3 with Bootstrap (implied)
- Scripting: Vanilla JavaScript
- UI Framework: Bootstrap (for responsive design)

**DevOps:**
- Containerization: Docker
- Orchestration: Docker Compose
- Version Control: Git

---

## Core Components

### 1. Database Abstraction Layer (`models/database.py`)

**Purpose:** Provides unified interface for MySQL and PostgreSQL

**Features:**
- Automatic fallback from MySQL to PostgreSQL (Supabase)
- Connection pooling & management
- Schema auto-initialization
- Transaction support (commit/rollback)

**Methods:**
```python
db.connect()              # Establish connection
db.execute(query, params) # Execute INSERT/UPDATE/DELETE
db.fetchone(query, params) # Fetch single record
db.fetchall(query, params) # Fetch multiple records
db.commit()               # Commit transaction
db.rollback()             # Rollback transaction
```

---

### 2. User Service (`services/user_service.py`)

**Purpose:** User management and authentication

**Key Methods:**
```python
UserService.create_user(name, mobile, password)
UserService.authenticate_user(mobile, password)
UserService.get_user_by_id(user_id)
UserService.update_profile(user_id, name)
UserService.change_password(user_id, old_pwd, new_pwd)
UserService.get_all_users()               # Admin only
UserService.get_total_users()             # Admin only
UserService.get_total_balance()           # Admin only
```

---

### 3. Transaction Service (`services/transaction_service.py`)

**Purpose:** Money transfer and deposit operations

**Key Methods:**
```python
TransactionService.transfer_money(sender_id, receiver_mobile, amount)
TransactionService.deposit_money(user_id, amount)
TransactionService.get_user_transactions(user_id, limit)
TransactionService.get_all_transactions(limit)        # Admin only
TransactionService.get_total_transactions_count()     # Admin only
TransactionService.delete_transaction(transaction_id) # Admin only
```

---

### 4. Routes (Blueprints)

#### Auth Routes (`routes/auth.py`)
- `POST /register` - New user registration
- `POST /login` - User login
- `GET /logout` - User logout

#### User Routes (`routes/user.py`)
- `GET /dashboard` - User dashboard (balance, recent transactions)
- `GET /profile` - User profile page
- `POST /profile` - Update profile or change password
- `GET /history` - Transaction history

#### Transaction Routes (`routes/transaction.py`)
- `GET/POST /transfer` - Money transfer form and processing
- `GET/POST /deposit` - Deposit form and processing
- `GET /download-statement` - PDF statement download

#### Admin Routes (`routes/admin.py`)
- `GET /admin` - Admin dashboard
- `GET /delete-transaction/<id>` - Delete transaction

#### API Routes (`routes/api.py`)
- `GET /api/get-balance` - Get user balance (JSON)
- `GET /api/live-transactions` - Get live transactions (JSON)

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    mobile VARCHAR(15) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL (hashed),
    balance DECIMAL(15, 2) DEFAULT 0.00,
    role VARCHAR(10) DEFAULT 'user'  -- 'user' or 'admin'
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);
```

---

## Data Flow

### Registration Flow
1. User fills register form
2. POST `/register` with credentials
3. UserService validates and hashes password
4. Creates user in database
5. Redirects to login page

### Login Flow
1. User enters mobile & password
2. POST `/login`
3. UserService authenticates credentials
4. Flask session created with user_id
5. Redirects to dashboard

### Transfer Flow
1. User selects receiver and amount
2. POST `/transfer`
3. TransactionService validates:
   - Sender balance sufficient
   - Receiver exists
   - Not self-transfer
4. Updates both user balances (atomic transaction)
5. Records transaction in database
6. Returns success page

### Admin Access
1. User must have `role = 'admin'`
2. Admin routes check role before displaying data
3. Can view all users and transactions
4. Can delete transactions (audit trail maintained)

---

## Configuration

### Environment Variables (`.env`)

```env
# Flask
SECRET_KEY=your_secret_key

# MySQL (Primary)
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DATABASE=airtel_payment_bank
MYSQL_PORT=3306

# PostgreSQL via Supabase (Fallback)
SUPABASE_DB_URL=postgresql://user:pass@host:port/db
```

### Settings Loader (`config/settings.py`)
- Loads from `.env` file using python-dotenv
- Provides defaults for missing variables
- Accessible via `settings.VARIABLE_NAME`

---

## Security Features

### Authentication
- Session-based using Flask sessions
- HTTP-only cookies (secure by default)
- Session timeout (browser close)

### Password Security
- Hashed using Werkzeug PBKDF2
- Never stored in plain text
- Changed via secure form with validation

### Database
- Parameterized queries (prevents SQL injection)
- Foreign key constraints
- Cascading deletes

### Authorization
- Role-based access control (user vs admin)
- Protected routes check session
- Admin operations verified

### CSRF Protection
- SECRET_KEY used for token generation
- Form tokens embedded in templates

---

## Deployment Considerations

### Development
- Flask development server
- Debug mode enabled
- Local MySQL database

### Production
- Gunicorn application server
- Nginx reverse proxy
- SSL/TLS certificates
- Environment-specific .env
- Managed database (Supabase/RDS)
- Error logging
- Request logging
- Health monitoring

---

## Performance Optimizations

### Database
- Connection pooling
- Parameterized queries
- Indexed mobile field (unique)
- Lazy loading of user data

### Frontend
- Static file caching
- CSS minification (can be added)
- JavaScript minification (can be added)
- Image optimization

### Application
- Session management
- Template caching

---

## Future Enhancements

### Feature Improvements
- [ ] OTP verification for registration
- [ ] Two-factor authentication
- [ ] Transaction encryption
- [ ] Real payment gateway integration
- [ ] Mobile app (React Native)
- [ ] Notifications (email, SMS)
- [ ] Analytics dashboard
- [ ] User referral program

### Technical Improvements
- [ ] Unit tests
- [ ] Integration tests
- [ ] API rate limiting
- [ ] Caching layer (Redis)
- [ ] Message queue (Celery)
- [ ] Real-time updates (WebSockets)
- [ ] GraphQL API
- [ ] API versioning

### Operations
- [ ] Comprehensive logging
- [ ] APM monitoring (New Relic, DataDog)
- [ ] Error tracking (Sentry)
- [ ] Database backups
- [ ] CI/CD pipeline
- [ ] Load testing
- [ ] Security audits

---

## Common Tasks

### Adding a New Route
1. Create function in appropriate file in `routes/`
2. Use `@blueprint.route()` decorator
3. Add corresponding template in `templates/`
4. Register blueprint in `app.py` (if new)

### Adding New Database Query
1. Add method to service in `services/`
2. Use `db.execute()`, `db.fetchone()`, or `db.fetchall()`
3. Always use parameterized queries with `%s` placeholders

### Creating New Template
1. Create `.html` file in `templates/`
2. Extend `base.html` for consistency
3. Use Jinja2 templating syntax
4. Reference static files with `{{ url_for('static', ...) }}`

### Debugging
- Check logs in console output
- Use Flask debug mode
- Add `print()` statements
- Use browser developer tools
- Check database directly with MySQL client

---

## File Sizes & Performance

- Main app: ~50KB
- Database layer: ~8KB
- Services: ~10KB
- Routes: ~15KB
- Templates: ~50KB
- Static CSS: ~30KB
- Total Python: ~100KB
- Total Frontend: ~80KB

---

## Support & Documentation

- **Setup:** See SETUP.md
- **Installation:** See INSTALLATION.md
- **API:** See API_DOCUMENTATION.md
- **Project:** This file
- **Code Comments:** Inline in source files

---

## License

See LICENSE file in repository

---

## Contributing

Contributions welcome! See CONTRIBUTING.md for guidelines.
