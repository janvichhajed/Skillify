from flask import Flask, render_template, redirect, session, url_for
from flask_cors import CORS
from config import Config
import os

from routes.auth_routes import auth_bp
from routes.skill_routes import skill_bp
from routes.session_routes import session_bp
from routes.verification_routes import verification_bp
from routes.certificate_routes import certificate_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Ensure upload directories exist
os.makedirs(app.config["CERTIFICATES_FOLDER"], exist_ok=True)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(skill_bp)
app.register_blueprint(session_bp)
app.register_blueprint(verification_bp)
app.register_blueprint(certificate_bp)

# Main Application Routes
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("auth.login_page"))

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))
    return render_template("dashboard.html", current_user=session)

@app.route("/browse_skills")
def browse_skills_page():
    return render_template("browse_skills.html", current_user=session.get("user_id"))

@app.route("/login")
def login_redirect():
    return redirect(url_for("auth.login_page"))

@app.route("/signup")
def signup_redirect():
    return redirect(url_for("auth.signup_page"))

@app.route("/profile")
def profile_page():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))
    return render_template("profile.html", current_user=session)

if __name__ == "__main__":
    app.run(debug=True)