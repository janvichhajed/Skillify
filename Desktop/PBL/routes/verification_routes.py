from flask import Blueprint, request, render_template, redirect, session, jsonify
from database.db import proofs, users, db
from models.proof_model import Proof
from bson import ObjectId
from services.github_verification import verify_github_profile
from services.credibility_score import calculate_credibility_score

verification_bp = Blueprint("verification", __name__, url_prefix="/verify")

@verification_bp.route("/", methods=["GET", "POST"])
def verify_page():
    if "user_id" not in session:
        return redirect("/auth/login")
        
    if request.method == "POST":
        github_url = request.form.get("github_url")
        portfolio_url = request.form.get("portfolio_url")
        cert_url = request.form.get("cert_url")
        
        # Calculate github score automatically
        gh_score = verify_github_profile(github_url) if github_url else 0
        
        proof = Proof(
            user_id=session["user_id"],
            github_url=github_url,
            portfolio_url=portfolio_url,
            cert_url=cert_url
        )
        proof.github_score = gh_score
        
        proofs.insert_one(proof.to_dict())
        
        return redirect("/profile")
        
    # GET
    return render_template("verify_skill.html", current_user=session)

@verification_bp.route("/admin", methods=["GET"])
def admin_verification():
    if session.get("user_role") != "admin":
        return "Unauthorized. Admin only.", 403
        
    pending_proofs = list(proofs.find({"status": "pending"}))
    return render_template("admin_verification.html", proofs=pending_proofs)

@verification_bp.route("/admin/<proof_id>/approve", methods=["POST"])
def approve_proof(proof_id):
    if session.get("user_role") != "admin":
        return "Unauthorized", 403
        
    proof = proofs.find_one({"_id": ObjectId(proof_id)})
    if proof:
        proofs.update_one({"_id": ObjectId(proof_id)}, {"$set": {"status": "approved"}})
        users.update_one({"_id": ObjectId(proof["user_id"])}, {"$set": {"verified": True}})
        
        # Recalculate credibility
        calculate_credibility_score(proof["user_id"], db)
        
    return redirect("/verify/admin")
