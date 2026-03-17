from flask import Blueprint, request, jsonify, render_template

verification_bp = Blueprint("verification", __name__, url_prefix="/verify")

@verification_bp.route("/github", methods=["POST"])
def verify_github():
    # Logic for verifying user through github activity
    return jsonify({"message": "GitHub verification endpoint"})

@verification_bp.route("/skill", methods=["GET", "POST"])
def verify_skill():
    if request.method == "POST":
        # logic to submit skill for verification
        return jsonify({"message": "Skill verification submitted"})
    
    return render_template("verify_skill.html")
