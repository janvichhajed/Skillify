from flask import Blueprint, request, jsonify, render_template

certificate_bp = Blueprint("certificate", __name__, url_prefix="/certificates")

@certificate_bp.route("/", methods=["GET", "POST"])
def manage_certificates():
    if request.method == "POST":
        return jsonify({"message": "Certificate generated"})
        
    return render_template("certificate.html")

@certificate_bp.route("/<cert_id>/verify", methods=["GET"])
def verify_certificate(cert_id):
    return render_template("verify_certificate.html", cert_id=cert_id)

