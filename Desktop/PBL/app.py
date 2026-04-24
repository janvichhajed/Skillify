from flask import Flask, render_template, redirect, session, url_for, jsonify
from flask_cors import CORS
from config import Config
from database.db import skills, users, sessions as sessions_col
import os
from dotenv import load_dotenv

load_dotenv()

from routes.auth_routes import auth_bp
from routes.skill_routes import skill_bp
from routes.session_routes import session_bp
from routes.verification_routes import verification_bp
from routes.certificate_routes import certificate_bp
from routes.admin_routes import admin_bp

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
app.register_blueprint(admin_bp)

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
    from bson import ObjectId
    from datetime import date, datetime
    uid  = session["user_id"]
    user = users.find_one({"_id": ObjectId(uid)})
    pending_count = sessions_col.count_documents({"provider_id": uid, "status": "pending"})
    active_count  = sessions_col.count_documents({"provider_id": uid, "status": "accepted"})

    # Find sessions scheduled for today
    today_str = date.today().isoformat()   # "2026-04-24"
    all_today = []
    for s in sessions_col.find({"status": "accepted", "$or": [
            {"provider_id": uid}, {"requester_id": uid}
        ]}):
        sched = s.get("scheduled_at", "")
        if sched and str(sched)[:10] == today_str:
            # get the other party's name
            other_id = s["requester_id"] if s["provider_id"] == uid else s["provider_id"]
            try:
                other = users.find_one({"_id": ObjectId(other_id)})
                s["other_name"] = other.get("user_name", "Unknown") if other else "Unknown"
            except:
                s["other_name"] = "Unknown"
            all_today.append(s)

    return render_template("dashboard.html",
        current_user=session,
        user=user,
        pending_sessions_count=pending_count,
        active_sessions_count=active_count,
        todays_sessions=all_today
    )

@app.route("/api/todays-sessions")
def todays_sessions_api():
    """Called by JS on page load to trigger browser notifications."""
    if "user_id" not in session:
        return jsonify({"sessions": []})
    from bson import ObjectId
    from datetime import date
    uid       = session["user_id"]
    today_str = date.today().isoformat()
    result    = []
    for s in sessions_col.find({"status": "accepted", "$or": [
            {"provider_id": uid}, {"requester_id": uid}
        ]}):
        sched = s.get("scheduled_at", "")
        if sched and str(sched)[:10] == today_str:
            try:
                other_id = s["requester_id"] if s["provider_id"] == uid else s["provider_id"]
                other = users.find_one({"_id": ObjectId(other_id)})
                other_name = other.get("user_name", "Unknown") if other else "Unknown"
            except:
                other_name = "Unknown"
            result.append({
                "id":           str(s["_id"]),
                "other_name":   other_name,
                "scheduled_at": str(sched),
                "meeting_link": s.get("meeting_link", ""),
                "meeting_type": s.get("meeting_type", "")
            })
    return jsonify({"sessions": result})

@app.route("/browse_skills")
def browse_skills_page():
    all_skills = list(skills.find())
    return render_template("browse_skills.html", skills=all_skills, current_user=session.get("user_id"))

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
    from bson import ObjectId
    user = users.find_one({"_id": ObjectId(session["user_id"])})
    my_skills = list(skills.find({"user_id": session["user_id"]}))
    return render_template("profile.html", current_user=session, user=user, my_skills=my_skills)

@app.route("/sessions-dashboard")
def sessions_dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))
    uid = session["user_id"]
    # Incoming requests (user is the provider)
    incoming = list(sessions_col.find({"provider_id": uid}).sort("created_at", -1))
    # Outgoing requests (user is the requester)
    outgoing = list(sessions_col.find({"requester_id": uid}).sort("created_at", -1))
    # Enrich with user names
    from bson import ObjectId
    def get_name(uid_str):
        try:
            u = users.find_one({"_id": ObjectId(uid_str)})
            return u.get("name", u.get("user_name", "Unknown")) if u else "Unknown"
        except:
            return "Unknown"
    for s in incoming:
        s["requester_name"] = get_name(s.get("requester_id", ""))
    for s in outgoing:
        s["provider_name"] = get_name(s.get("provider_id", ""))
    return render_template("sessions_dashboard.html",
        current_user=session, incoming=incoming, outgoing=outgoing)

@app.route("/api/notifications")
def notifications_api():
    if "user_id" not in session:
        return jsonify({"count": 0})
    uid = session["user_id"]
    pending = sessions_col.count_documents({"provider_id": uid, "status": "pending"})
    return jsonify({"count": pending})

if __name__ == "__main__":
    app.run(debug=True)