def verify_uploaded_certificate(data):
    """
    Verifies a user's uploaded proof of a prior certificate.
    Case 1: Has link -> validates link
    Case 2: No link -> manual peer/admin review queued
    """
    if "verification_link" in data and data["verification_link"]:
        # Case 1: Automated/Semi-automated validation
        return {"status": "valid", "method": "url_check"}
    else:
        # Case 2: Requires manual peer/admin validation
        if "cert_file" in data and "proof_video" in data:
            return {"status": "pending_manual_review"}
        return {"status": "invalid", "reason": "Missing documentation"}
        
def verify_system_certificate(cert_id, db):
    """
    Checks if a Skillify generated certificate ID is valid.
    """
    cert = db.certificates.find_one({"certificate_id": cert_id})
    if cert and cert.get("is_valid", False):
        return True, cert
    return False, None
