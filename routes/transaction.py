import io
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, session, flash, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes

from services.user_service import UserService
from services.transaction_service import TransactionService

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route("/transfer", methods=["GET", "POST"])
def transfer():
    if "user_id" not in session:
        return redirect("/login")

    sender_id = session["user_id"]
    sender = UserService.get_user_by_id(sender_id)

    if request.method == "POST":
        receiver_mobile = request.form.get("receiver_mobile")
        amount = float(request.form.get("amount", 0))

        success, msg_or_name = TransactionService.transfer_money(sender_id, receiver_mobile, amount)
        
        if success:
            return render_template("transfer_success.html", amount=amount, receiver_name=msg_or_name)
        else:
            flash(f"Transfer Failed: {msg_or_name} ❌", "danger")
            return redirect("/transfer")

    return render_template("transfer.html", balance=sender["balance"])

@transaction_bp.route("/deposit", methods=["GET", "POST"])
def deposit():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        user_id = session["user_id"]
        amount = float(request.form.get("amount", 0))

        success, msg = TransactionService.deposit_money(user_id, amount)
        
        if success:
            transaction_id = str(uuid.uuid4())[:8].upper()
            payment_time = datetime.now().strftime("%d %b %Y, %I:%M %p")
            return render_template("receipt.html", transaction_id=transaction_id, amount=amount, payment_time=payment_time, upi_id="adminbank@upi")
        else:
            flash(f"Deposit Failed: {msg} ❌", "danger")
            return redirect("/deposit")

    return render_template("deposit.html")

@transaction_bp.route("/download-statement")
def download_statement():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    user = UserService.get_user_by_id(user_id)
    transactions = TransactionService.get_user_transactions(user_id)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>Airtel Payments Bank - Statement</b>", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Account Holder: {user['full_name']}", styles["Normal"]))
    elements.append(Paragraph(f"Generated On: {datetime.now().strftime('%d %b %Y %I:%M %p')}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    data = [["Sender", "Receiver", "Amount (Rs)", "Date"]]
    for t in transactions:
        data.append([
            t["sender_name"],
            t["receiver_name"],
            str(t["amount"]),
            str(t["timestamp"])
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor('#e63946')),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="statement.pdf", mimetype="application/pdf")
