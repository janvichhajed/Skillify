from flask import Blueprint, request, jsonify, render_template, session, redirect
from database.db import sessions, db
from models.session_model import Session
from datetime import datetime
from bson import ObjectId
from services.credibility_score import calculate_credibility_score

session_bp = Blueprint("session", __name__, url_prefix="/sessions")

@session_bp.route("/request", methods=["POST"])
def request_session():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    provider_id = request.form.get("provider_id")
    skill_id = request.form.get("skill_id")
    scheduled_at = request.form.get("scheduled_at")
    
    new_sess = Session(session["user_id"], provider_id, skill_id, scheduled_at)
    sessions.insert_one(new_sess.to_dict())
    return redirect("/dashboard")

@session_bp.route("/<session_id>/accept", methods=["POST"])
def accept_session(session_id):
    sessions.update_one({"_id": ObjectId(session_id)}, {"$set": {"status": "accepted"}})
    return redirect("/dashboard")

@session_bp.route("/<session_id>/complete", methods=["POST"])
def complete_session(session_id):
    sessions.update_one(
        {"_id": ObjectId(session_id)}, 
        {"$set": {"status": "completed", "completed_at": datetime.utcnow()}}
    )
    # Recalulate credibility
    sess = sessions.find_one({"_id": ObjectId(session_id)})
    if sess:
        calculate_credibility_score(sess["provider_id"], db)
    return redirect("/dashboard")

@session_bp.route("/<session_id>/feedback", methods=["GET", "POST"])
def submit_feedback(session_id):
    if request.method == "POST":
        rating = int(request.form.get("rating"))
        review_text = request.form.get("review_text")
        
        sess = sessions.find_one({"_id": ObjectId(session_id)})
        if not sess:
            return "Session not found", 404
            
        from models.feedback_model import Feedback
        fb = Feedback(session_id, session["user_id"], sess["provider_id"], rating, review_text)
        db.feedback.insert_one(fb.to_dict())
        
        sessions.update_one({"_id": ObjectId(session_id)}, {"$set": {"feedback_given": True}})
        calculate_credibility_score(sess["provider_id"], db)
        
        return redirect("/dashboard")
        
    return render_template("feedback.html", session_id=session_id)
