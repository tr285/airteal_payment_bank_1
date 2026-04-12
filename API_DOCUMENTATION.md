# Airtel Payment Bank - API Documentation

## Overview
REST API endpoints for the Airtel Payment Bank application. All endpoints are protected with session-based authentication.

---

## Base URL
```
http://localhost:5000
http://your-domain.com
```

---

## Authentication
All API endpoints require an active user session. Sessions are managed via HTTP cookies set during login.

### Login Flow
1. POST `/login` with credentials
2. Session cookie is automatically set
3. Use session for subsequent requests
4. Logout with `/logout`

---

## API Endpoints

### Health Check
**Endpoint:** `GET /health`

**Description:** Check if API and database are operational

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

**Status Codes:**
- 200: Healthy
- 500: Unhealthy (database error)

---

### User Balance
**Endpoint:** `GET /api/get-balance`

**Description:** Get current user's account balance

**Response:**
```json
{
  "balance": 5000.50
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 404: User not found

**Example:**
```bash
curl http://localhost:5000/api/get-balance \
  -b "session=your_session_cookie"
```

---

### Live Transactions
**Endpoint:** `GET /api/live-transactions`

**Description:** Get transactions for the current user (or all if admin)

**Query Parameters:**
- None required

**Response (User):**
```json
{
  "transactions": [
    {
      "id": 1,
      "amount": 500.00,
      "timestamp": "12 Apr 2026, 03:30 PM",
      "sender_name": "Admin User",
      "receiver_name": "Raj Kumar",
      "is_credit": true
    }
  ]
}
```

**Response (Admin):**
```json
{
  "transactions": [
    {
      "id": 1,
      "amount": 500.00,
      "timestamp": "12 Apr 2026, 03:30 PM",
      "sender_name": "Raj Kumar",
      "receiver_name": "Priya Singh",
      "is_credit": false
    }
  ]
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized

**Example:**
```bash
curl http://localhost:5000/api/live-transactions \
  -b "session=your_session_cookie" \
  -H "Content-Type: application/json"
```

---

## Authentication Endpoints

### Register
**Endpoint:** `POST /register`

**Parameters:**
```json
{
  "full_name": "John Doe",
  "mobile": "9123456789",
  "password": "password123"
}
```

**Response:**
- Redirect to `/login` on success
- Flash message: "Registration Successful"

**Validation:**
- Mobile number must be unique
- Mobile must be 10-15 digits
- Password must be at least 6 characters

---

### Login
**Endpoint:** `POST /login`

**Parameters:**
```json
{
  "mobile": "9123456789",
  "password": "password123"
}
```

**Response:**
- Redirect to `/dashboard` on success
- Session cookie set automatically

**Status:**
- Success: Redirect to dashboard
- Failure: Redirect to login with error message

---

### Logout
**Endpoint:** `GET /logout`

**Response:**
- Redirect to `/login`
- Session cleared

---

## User Endpoints

### Dashboard
**Endpoint:** `GET /dashboard`

**Response:** HTML page with:
- User balance
- Recent transactions (last 5)
- Total deposits
- Total transfers sent

**Requires:** Active session

---

### Profile
**Endpoint:** `GET /profile`

**Response:** User profile page with:
- Name
- Mobile number
- Balance
- Options to update profile
- Option to change password

**Update Profile:**
**POST /profile**
```json
{
  "full_name": "New Name",
  "update_profile": "true"
}
```

**Change Password:**
**POST /profile**
```json
{
  "current_password": "old123",
  "new_password": "new123",
  "confirm_password": "new123",
  "change_password": "true"
}
```

---

### Transaction History
**Endpoint:** `GET /history`

**Response:** HTML page showing:
- All user transactions (sent and received)
- Transaction IDs
- Amounts
- Timestamps
- Transaction types

---

## Transaction Endpoints

### Transfer Money
**Endpoint:** `POST /transfer`

**Parameters:**
```json
{
  "receiver_mobile": "9198765432",
  "amount": 500.00
}
```

**Response:**
- Success: Shows transfer receipt page
- Failure: Redirect to transfer page with error

**Validation:**
- Amount must be > 0
- Receiver must exist
- Sender must have sufficient balance
- Cannot transfer to self

**Errors:**
- "Invalid amount"
- "Insufficient balance"
- "Receiver not found"
- "Cannot send money to yourself"

---

### Deposit Money
**Endpoint:** `POST /deposit`

**Parameters:**
```json
{
  "amount": 1000.00
}
```

**Response:**
- Success: Shows deposit receipt
- Failure: Redirect to deposit page with error

**Validation:**
- Amount must be > 0
- Admin account must exist

---

### Download Statement
**Endpoint:** `GET /download-statement`

**Response:**
- PDF file download
- Contains transaction history
- Account holder information
- Generation timestamp

**Content-Type:** `application/pdf`

---

## Admin Endpoints

### Admin Panel
**Endpoint:** `GET /admin`

**Requires:** Admin role

**Response:** Dashboard with:
- Total users count
- Total transactions count
- Total balance in system
- List of all users
- List of all transactions (last 100)

---

### Delete Transaction
**Endpoint:** `GET /delete-transaction/<transaction_id>`

**Requires:** Admin role

**Parameters:**
- `transaction_id` (URL parameter): ID of transaction to delete

**Response:**
- Redirect to admin panel
- Success message

**Note:** Only admins can delete transactions

---

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Unauthorized"
}
```
**Cause:** Not logged in or session expired

### 404 Not Found
```json
{
  "error": "User not found"
}
```

### 500 Server Error
```json
{
  "error": "Internal server error message"
}
```

---

## Rate Limiting
Currently no rate limiting implemented. Production deployment should include:
- Request rate limiting (e.g., 100 requests/minute per IP)
- Transaction limits per user
- Login attempt limiting (max 5 attempts per 15 minutes)

---

## Security Considerations

### HTTPS
Always use HTTPS in production to encrypt data in transit.

### Session Management
- Sessions expire after browser close (configurable)
- Session cookies are HTTP-only
- CSRF protection enabled via SECRET_KEY

### Input Validation
- All inputs are validated before processing
- SQL injection prevented via parameterized queries
- XSS protection via template escaping

### Password Security
- Passwords hashed using Werkzeug security
- Never stored in plain text
- Minimum length enforced

---

## Example Usage

### Using cURL

**Login:**
```bash
curl -c cookies.txt -X POST http://localhost:5000/login \
  -d "mobile=9123456789&password=user123"
```

**Get Balance:**
```bash
curl -b cookies.txt http://localhost:5000/api/get-balance
```

**Transfer Money:**
```bash
curl -b cookies.txt -X POST http://localhost:5000/transfer \
  -d "receiver_mobile=9198765432&amount=500"
```

### Using Python
```python
import requests

session = requests.Session()

# Login
response = session.post('http://localhost:5000/login', data={
    'mobile': '9123456789',
    'password': 'user123'
})

# Get balance
response = session.get('http://localhost:5000/api/get-balance')
print(response.json())

# Transfer money
response = session.post('http://localhost:5000/transfer', data={
    'receiver_mobile': '9198765432',
    'amount': 500
})
```

### Using JavaScript/Fetch
```javascript
// Login
const loginResponse = await fetch('http://localhost:5000/login', {
  method: 'POST',
  credentials: 'include',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: 'mobile=9123456789&password=user123'
});

// Get balance
const balanceResponse = await fetch('http://localhost:5000/api/get-balance', {
  credentials: 'include'
});
const data = await balanceResponse.json();
console.log('Balance:', data.balance);
```

---

## Changelog

### v1.0.0 (Current)
- Initial release
- Core banking features
- Admin dashboard
- PDF statement generation

---

## Support
For issues or questions about the API, please create an issue in the repository or contact support.
