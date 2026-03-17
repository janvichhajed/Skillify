from flask import Flask, render_template
from flask_cors import CORS

from routes.auth_routes import auth_bp
from routes.skill_routes import skill_bp
from routes.session_routes import session_bp
from routes.verification_routes import verification_bp
from routes.certificate_routes import certificate_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(skill_bp)
app.register_blueprint(session_bp)
app.register_blueprint(verification_bp)
app.register_blueprint(certificate_bp)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/browse_skills")
def browse_skills_page():
    return render_template("browse_skills.html")

@app.route("/profile")
def profile_page():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)