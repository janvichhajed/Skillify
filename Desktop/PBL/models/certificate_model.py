from datetime import datetime

class Certificate:
    def __init__(self, user_id, skill_id, issued_by, certificate_hash):
        self.user_id = user_id
        self.skill_id = skill_id
        self.issued_by = issued_by
        self.issued_date = datetime.utcnow()
        self.certificate_hash = certificate_hash
        self.is_valid = True

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "skill_id": self.skill_id,
            "issued_by": self.issued_by,
            "issued_date": self.issued_date,
            "certificate_hash": self.certificate_hash,
            "is_valid": self.is_valid
        }
