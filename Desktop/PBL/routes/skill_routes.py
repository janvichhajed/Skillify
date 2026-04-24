from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from database.db import skills, users, proofs
from models.skill_model import Skill
from bson import ObjectId

skill_bp = Blueprint("skill", __name__, url_prefix="/skills")

@skill_bp.route("/", methods=["GET"])
def browse_skills():
    all_skills = list(skills.find())
    for s in all_skills:
        try:
            p = users.find_one({"_id": ObjectId(s["user_id"])})
            s["provider_name"] = p.get("name", f"User {str(p['_id'])[:4]}") if p else "Unknown User"
            s["is_verified"] = p.get("verified", False) if p else False
        except:
            s["provider_name"] = "Unknown User"
            s["is_verified"] = False
            
    return render_template("browse_skills.html", skills=all_skills, current_user=session)

@skill_bp.route("/post", methods=["GET", "POST"])
def post_skill():
    if "user_id" not in session:
        return redirect("/auth/login")
        
    if session.get("user_role") not in ["teach", "both"]:
        return redirect("/dashboard")
    
    # Fetch the user and check verified status
    user = users.find_one({"_id": ObjectId(session["user_id"])})
    is_verified = user.get("verified", False) if user else False

    # Fetch the approved proof to get the verified category
    approved_proof = proofs.find_one({
        "user_id": session["user_id"],
        "status": "approved"
    })
    verified_category = approved_proof.get("category") if approved_proof else None

    error = None

    if request.method == "POST":
        # If not verified, block posting
        if not is_verified:
            return redirect("/verify/")
        
        title = request.form.get("title")
        description = request.form.get("description")
        category = request.form.get("category")
        proficiency = request.form.get("proficiency")

        # Category must match the verified category
        if verified_category and category != verified_category:
            error = f"You can only post skills in your verified category: '{verified_category}'. Please select the correct category."
            return render_template(
                "post_skill.html",
                current_user=session,
                is_verified=is_verified,
                verified_category=verified_category,
                error=error
            )
        
        new_skill = Skill(session["user_id"], title, description, category, proficiency)
        skills.insert_one(new_skill.to_dict())
        return redirect("/browse_skills")
        
    return render_template(
        "post_skill.html",
        current_user=session,
        is_verified=is_verified,
        verified_category=verified_category,
        error=error
    )

@skill_bp.route("/delete/<skill_id>", methods=["POST"])
def delete_skill(skill_id):
    if "user_id" not in session:
        return redirect("/auth/login")
    
    # Only allow the owner to delete
    skill = skills.find_one({"_id": ObjectId(skill_id)})
    if skill and skill["user_id"] == session["user_id"]:
        skills.delete_one({"_id": ObjectId(skill_id)})
    
    return redirect("/browse_skills")
