from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
import os
import uuid

def generate_certificate(mentor_name, learner_name, skill_title, date_str, output_folder):
    """
    Generates a PDF certificate after a successful session.
    Returns:
        certificate_id: unique ID string
        filepath: absolute path to the generated PDF
    """
    cert_id = str(uuid.uuid4())[:12].upper()
    filename = f"certificate_{cert_id}.pdf"
    filepath = os.path.join(output_folder, filename)
    
    c = canvas.Canvas(filepath, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Border
    c.setLineWidth(5)
    c.rect(20, 20, width - 40, height - 40)
    
    # Title
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(width / 2.0, height - 100, "Certificate of Completion")
    
    # Subtitle
    c.setFont("Helvetica", 24)
    c.drawCentredString(width / 2.0, height - 160, "This is to certify that")
    
    # Learner Name
    c.setFont("Helvetica-Bold", 35)
    c.drawCentredString(width / 2.0, height - 220, learner_name)
    
    # Course info
    c.setFont("Helvetica", 20)
    c.drawCentredString(width / 2.0, height - 280, f"has successfully completed a peer-to-peer session on")
    
    # Skill Name
    c.setFont("Helvetica-Bold", 25)
    c.drawCentredString(width / 2.0, height - 330, skill_title)
    
    # Mentor
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2.0, height - 390, f"Mentored by: {mentor_name}")
    
    # Date and ID
    c.setFont("Helvetica", 14)
    c.drawString(100, 100, f"Date: {date_str}")
    c.drawRightString(width - 100, 100, f"Credential ID: {cert_id}")
    
    c.save()
    
    return cert_id, filename
