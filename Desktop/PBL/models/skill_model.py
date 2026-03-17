from datetime import datetime

class Skill:
    def __init__(self, user_id, title, description, category, proficiency="beginner"):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.category = category
        self.proficiency = proficiency
        self.is_verified = False
        self.endorsements = 0
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "proficiency": self.proficiency,
            "is_verified": self.is_verified,
            "endorsements": self.endorsements,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        skill = cls(
            user_id=data.get("user_id"),
            title=data.get("title"),
            description=data.get("description"),
            category=data.get("category"),
            proficiency=data.get("proficiency", "beginner")
        )
        skill.is_verified = data.get("is_verified", False)
        skill.endorsements = data.get("endorsements", 0)
        skill.created_at = data.get("created_at")
        return skill
