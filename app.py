from flask import Flask, redirect
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)