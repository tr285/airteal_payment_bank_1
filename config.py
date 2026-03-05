import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tukaram143",
    database="airtel_payment_bank"
)

cursor = db.cursor()