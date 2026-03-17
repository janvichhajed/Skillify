from flask import Blueprint, request, jsonify, render_template, session, redirect
from database.db import skills, users
from models.skill_model import Skill

skill_bp = Blueprint("skill", __name__, url_prefix="/skills")

@skill_bp.route("/", methods=["GET"])
def browse_skills():
    all_skills = list(skills.find())
    return render_template("browse_skills.html", skills=all_skills, current_user=session)

@skill_bp.route("/post", methods=["GET", "POST"])
def post_skill():
    if "user_id" not in session:
        return redirect("/auth/login")
        
    # Check if mentor
    user = users.find_one({"_id": session["user_id"]})
    # Optional logic: only verified mentors can post skills
    
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        category = request.form.get("category")
        proficiency = request.form.get("proficiency")
        
        new_skill = Skill(session["user_id"], title, description, category, proficiency)
        skills.insert_one(new_skill.to_dict())
        return redirect("/skills")
        
    return render_template("post_skill.html", current_user=session)
