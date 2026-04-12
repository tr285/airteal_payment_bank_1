from flask import Blueprint, render_template, redirect, session, flash
from services.user_service import UserService
from services.transaction_service import TransactionService

admin_bp = Blueprint('admin', __name__)

def is_admin():
    if "user_id" not in session:
        return False
    user = UserService.get_user_by_id(session["user_id"])
    return user and user["role"] == "admin"

@admin_bp.route("/admin")
def admin_panel():
    if not is_admin():
        flash("Access Denied ❌", "danger")
        return redirect("/dashboard")

    total_users = UserService.get_total_users()
    total_transactions = TransactionService.get_total_transactions_count()
    total_balance = UserService.get_total_balance()
    
    users = UserService.get_all_users()
    transactions = TransactionService.get_all_transactions(limit=100)

    return render_template(
        "admin.html",
        total_users=total_users,
        total_transactions=total_transactions,
        total_balance=total_balance,
        users=users,
        transactions=transactions
    )

@admin_bp.route("/delete-transaction/<int:transaction_id>")
def delete_transaction(transaction_id):
    if not is_admin():
        flash("Access Denied ❌", "danger")
        return redirect("/dashboard")

    TransactionService.delete_transaction(transaction_id)
    flash("Transaction Deleted Successfully 🗑", "success")
    return redirect("/admin")
