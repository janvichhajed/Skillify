from datetime import datetime

class Session:
    def __init__(self, requester_id, provider_id, skill_id, scheduled_at=None):
        self.requester_id = requester_id
        self.provider_id = provider_id
        self.skill_id = skill_id
        self.status = "pending"  # pending, accepted, completed, cancelled
        self.scheduled_at = scheduled_at
        self.created_at = datetime.utcnow()
        self.completed_at = None
        self.feedback_given = False
        self.certificate_issued = False

    def to_dict(self):
        return {
            "requester_id": self.requester_id,
            "provider_id": self.provider_id,
            "skill_id": self.skill_id,
            "status": self.status,
            "scheduled_at": self.scheduled_at,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "feedback_given": self.feedback_given,
            "certificate_issued": self.certificate_issued
        }
    
    @classmethod
    def from_dict(cls, data):
        session = cls(
            requester_id=data.get("requester_id"),
            provider_id=data.get("provider_id"),
            skill_id=data.get("skill_id"),
            scheduled_at=data.get("scheduled_at")
        )
        session.status = data.get("status", "pending")
        session.created_at = data.get("created_at")
        session.completed_at = data.get("completed_at")
        session.feedback_given = data.get("feedback_given", False)
        session.certificate_issued = data.get("certificate_issued", False)
        return session
