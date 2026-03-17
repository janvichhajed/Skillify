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

    def to_dict(self):
        return {
            "requester_id": self.requester_id,
            "provider_id": self.provider_id,
            "skill_id": self.skill_id,
            "status": self.status,
            "scheduled_at": self.scheduled_at,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "feedback_given": self.feedback_given
        }
