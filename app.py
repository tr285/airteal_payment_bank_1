from flask import Flask, redirect, render_template
from config.settings import settings

# Initialize application
app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

# Register Blueprints
from routes.auth import auth_bp
from routes.user import user_bp
from routes.transaction import transaction_bp
from routes.admin import admin_bp
from routes.api import api_bp

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp, url_prefix='/api')

@app.route("/")
def home():
    return redirect("/login")

@app.route("/health")
def health():
    """Health check endpoint for monitoring"""
    try:
        from models.database import db
        # Test database connection
        db.fetchone("SELECT 1")
        return {"status": "healthy", "database": "connected"}, 200
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500

if __name__ == "__main__":
    print("[INFO] Starting Airtel Payment Bank application...")
    print("[INFO] Visit: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
