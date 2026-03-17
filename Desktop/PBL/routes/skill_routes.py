from flask import Blueprint, request, jsonify, render_template

skill_bp = Blueprint("skill", __name__, url_prefix="/skills")

@skill_bp.route("/", methods=["GET", "POST"])
def manage_skills():
    if request.method == "POST":
        # Add a new skill logic
        return jsonify({"message": "Skill added successfully"}), 201
        
    # Get list of skills
    return render_template("browse_skills.html")

@skill_bp.route("/<skill_id>", methods=["GET", "PUT", "DELETE"])
def skill_detail(skill_id):
    if request.method == "GET":
        return jsonify({"message": f"Details for skill {skill_id}"})
    elif request.method == "PUT":
        return jsonify({"message": f"Updated skill {skill_id}"})
    else:
        return jsonify({"message": f"Deleted skill {skill_id}"})
