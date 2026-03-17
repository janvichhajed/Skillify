from flask import Blueprint, request, jsonify, render_template

session_bp = Blueprint("session", __name__, url_prefix="/sessions")

@session_bp.route("/", methods=["GET", "POST"])
def manage_sessions():
    if request.method == "POST":
        # logic to request a new session
        return jsonify({"message": "Session created successfully"}), 201
        
    return render_template("session.html")

@session_bp.route("/<session_id>", methods=["GET", "PUT"])
def session_detail(session_id):
    if request.method == "GET":
        return jsonify({"message": f"Details for session {session_id}"})
    else:
        # Update session status
        return jsonify({"message": f"Updated session {session_id}"})
