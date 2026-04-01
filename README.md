# 🏦 Airtel Payment Bank (Full Stack Project)

A modern **Digital Banking Web Application** built using **Flask, MySQL, and Docker**.
This project simulates real-world banking features like money transfer, deposits, transaction history, and admin control.

---

## 🚀 Features

### 👤 User Features

* 🔐 Register & Login system
* 💰 Check account balance
* 💸 Transfer money to other users
* ➕ Add money via QR (UPI simulation)
* 📜 Transaction history
* 📄 Download bank statement (PDF)
* 👤 Profile management (update name & password)

---

### 🏦 Admin Features

* 👑 Admin dashboard
* 📊 View all users
* 💳 View all transactions
* 🗑 Delete transaction history
* 💰 Monitor total bank balance

---

### 🎨 UI Features

* 📱 Modern banking dashboard
* 📊 Interactive UI with animations
* 🌙 Dark mode support
* 📌 Sidebar navigation (like real banking apps)

---

## 🛠 Tech Stack

* **Frontend:** HTML, CSS, Bootstrap, JavaScript
* **Backend:** Flask (Python)
* **Database:** MySQL
* **PDF Generation:** ReportLab
* **Containerization:** Docker

---

## ⚙️ Installation (Local Setup)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/airtel_payment_bank.git
cd airtel_payment_bank
```

---

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Database

Edit `config.py`:

```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="airtel_bank"
)
```

---

### 5️⃣ Run Application

```bash
python app.py
```

Open browser:

```
http://localhost:5000
```

---

## 🐳 Run with Docker

### Build Image

```bash
docker build -t airtel-payment-bank .
```

### Run Container

```bash
docker run -p 5000:5000 airtel-payment-bank
```

---

## 📂 Project Structure

```
airtel_payment_bank/
│
├── app.py
├── config.py
├── requirements.txt
├── Dockerfile
│
├── templates/
├── static/
```

---

## 🔐 Future Improvements

* 🔑 OTP verification system
* 📲 Real payment gateway integration
* 📊 Advanced analytics dashboard
* 🔒 Security enhancements (JWT, encryption)
* ☁️ Cloud deployment (AWS / Render)

---

## 👨‍💻 Author

**Tukaram Gore**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
