from flask import Blueprint, request, render_template, session, redirect, current_app, jsonify, send_from_directory
from database.db import certificates, sessions, users, skills, db
from models.certificate_model import Certificate
from bson import ObjectId
from services.certificate_generator import generate_certificate
from services.certificate_verification import verify_system_certificate

certificate_bp = Blueprint("certificate", __name__, url_prefix="/certificates")

@certificate_bp.route("/")
def list_certificates():
    if "user_id" not in session:
        return redirect("/auth/login")
        
    user_certs = list(certificates.find({"learner_id": str(session["user_id"])}))
    
    # We also pass the user's name to display
    return render_template("certificate.html", certificates=user_certs)

@certificate_bp.route("/generate/<session_id>", methods=["POST"])
def generate(session_id):
    if "user_id" not in session:
        return redirect("/auth/login")
        
    sess = sessions.find_one({"_id": ObjectId(session_id)})
    if not sess or sess["status"] != "completed":
        return "Cannot generate certificate for incomplete session", 400
        
    if sess["certificate_issued"]:
        return "Certificate already issued", 400
        
    mentor = users.find_one({"_id": ObjectId(sess["provider_id"])})
    learner = users.find_one({"_id": ObjectId(sess["requester_id"])})
    skill = skills.find_one({"_id": ObjectId(sess["skill_id"])})
    
    # Generate the physical PDF
    date_str = sess["completed_at"].strftime("%B %d, %Y")
    cert_id, filename = generate_certificate(
        mentor_name=mentor["name"],
        learner_name=learner["name"],
        skill_title=skill["title"],
        date_str=date_str,
        output_folder=current_app.config["CERTIFICATES_FOLDER"]
    )
    
    # Save to MongoDB
    new_cert = Certificate(
        certificate_id=cert_id,
        mentor_id=str(mentor["_id"]),
        learner_id=str(learner["_id"]),
        skill_id=str(skill["_id"])
    )
    certificates.insert_one(new_cert.to_dict())
    
    # Mark session as issued and store ID
    sessions.update_one(
        {"_id": ObjectId(session_id)}, 
        {"$set": {"certificate_issued": True, "certificate_id": cert_id}}
    )
    
    return redirect("/dashboard")

@certificate_bp.route("/download/<cert_id>")
def download_cert(cert_id):
    filename = f"certificate_{cert_id}.pdf"
    return send_from_directory(current_app.config["CERTIFICATES_FOLDER"], filename)


