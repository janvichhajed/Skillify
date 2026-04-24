import os
import re
from flask import Blueprint, request, redirect, render_template, session, flash
from werkzeug.utils import secure_filename
from database.db import users, proofs
from datetime import datetime

verification_bp = Blueprint("verification", __name__)

UPLOAD_FOLDER = "static/uploads/certificates"
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

# Category → type mapping
TECHNICAL_CATEGORIES = {"Development", "Data Science", "Machine Learning", 
                        "Cybersecurity", "Blockchain", "Web Development"}
CREATIVE_CATEGORIES  = {"Design", "Marketing", "Other"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def auto_verify(email, skill_name, category, github, portfolio, experience, has_certificate=False):
    is_technical = category in TECHNICAL_CATEGORIES

    missing = []
    
    # Both tracks require an experience description
    if not experience or len(experience.strip()) < 5: 
        missing.append("experience description")
    
    if is_technical:
        # Technical requires GitHub. Portfolio & Certificate are optional.
        if not github: 
            missing.append("github profile link")
    else:
        # Creative requires Portfolio & Certificate. GitHub is optional.
        if not portfolio: 
            missing.append("portfolio link")
        if not has_certificate: 
            missing.append("uploaded certificate")
        
    if len(missing) == 0:
        decision = "Approved"
        score = 9.0
        reason = "All required proofs provided. Application approved."
    else:
        decision = "Rejected"
        score = 1.0
        reason = f"Missing required fields: {', '.join(missing)}"

    # Update database directly inside auto_verify to match final requested status
    if decision == "Approved":
        users.update_one(
            {"email": email},
            {"$set": {
                "verification_status": "Approved",
                "credibility_score":   7.0,
                "badge":               "Verified Mentor",
                "ai_verification_reason": reason,
                "ai_confidence":       score,
                "verified":            True
            }}
        )
    else:
        users.update_one(
            {"email": email},
            {"$set": {
                "verification_status": "Rejected",
                "credibility_score":   0.0,
                "badge":               "Not Verified",
                "ai_verification_reason": reason,
                "ai_confidence":       score,
                "verified":            False
            }}
        )

    proofs.find_one_and_update(
        {"email": email, "skill_name": skill_name},
        {"$set": {
            "status":        decision,
            "ai_decision":   decision,
            "ai_reason":     reason,
            "ai_confidence": score
        }},
        sort=[("submitted_at", -1)]
    )

    print(f"[verify] {email} | {category} | {decision} | score={score}")
    return decision, score, reason


@verification_bp.route("/verify-skill", methods=["GET", "POST"])
def verify_skill():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    if request.method == "POST":
        email          = request.form.get("email", "").strip()
        skill_name     = request.form.get("skill_name", "").strip()
        category       = request.form.get("category", "").strip()
        
        # Using the exact field names requested
        github     = request.form.get("github", "").strip()
        portfolio  = request.form.get("portfolio", "").strip()
        experience = request.form.get("experience", "").strip()

        certificate = request.files.get("certificate")
        file_path, has_certificate = "", False

        if certificate and allowed_file(certificate.filename):
            filename = secure_filename(certificate.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            certificate.save(save_path)
            file_path = save_path
            has_certificate = True

        # Save proof always first
        proofs.insert_one({
            "email":            email,
            "skill_name":       skill_name,
            "category":         category,
            "github_link":      github,
            "portfolio_link":   portfolio,
            "description":      experience,
            "certificate_file": file_path,
            "status":           "Pending Review",
            "submitted_at":     datetime.utcnow()
        })

        # Auto-verify
        try:
            decision, score, reason = auto_verify(
                email, skill_name, category,
                github, portfolio,
                experience, has_certificate
            )
            if decision == "Approved":
                flash(f"✅ Approved! Credibility Score: 90 — {reason}", "success")
            else:
                flash(f"❌ Rejected! Credibility Score: 40 — {reason}", "error")
        except Exception as e:
            print(f"[auto_verify] error: {e}")
            flash("Verification failed due to a system error.", "error")

        return redirect("/dashboard")

    return render_template("verify_skill.html")
