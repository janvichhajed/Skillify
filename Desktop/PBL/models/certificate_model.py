from datetime import datetime

class Certificate:
    def __init__(self, certificate_id, mentor_id, learner_id, skill_id):
        self.certificate_id = certificate_id
        self.mentor_id = mentor_id
        self.learner_id = learner_id
        self.skill_id = skill_id
        self.issue_date = datetime.utcnow()
        self.is_valid = True

    def to_dict(self):
        return {
            "certificate_id": self.certificate_id,
            "mentor_id": self.mentor_id,
            "learner_id": self.learner_id,
            "skill_id": self.skill_id,
            "issue_date": self.issue_date,
            "is_valid": self.is_valid
        }
        
    @classmethod
    def from_dict(cls, data):
        cert = cls(
            certificate_id=data.get("certificate_id"),
            mentor_id=data.get("mentor_id"),
            learner_id=data.get("learner_id"),
            skill_id=data.get("skill_id")
        )
        cert.issue_date = data.get("issue_date")
        cert.is_valid = data.get("is_valid", True)
        return cert
