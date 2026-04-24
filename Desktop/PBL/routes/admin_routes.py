from flask import Blueprint, render_template, request, redirect
from database.db import users, proofs

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/verifications")
def admin_verifications():
    all_proofs = list(proofs.find().sort("submitted_at", -1))
    return render_template("admin_verifications.html", proofs=all_proofs)

@admin_bp.route("/admin/update-status", methods=["POST"])
def update_status():
    email = request.form.get("email")
    skill = request.form.get("skill_name")
    new_status = request.form.get("status")

    proofs.update_one(
        {"email": email, "skill_name": skill},
        {"$set": {"status": new_status}}
    )
    users.update_one(
        {"email": email},
        {"$set": {"verification_status": new_status}}
    )
    return redirect("/admin/verifications")
