class Skill:
    def __init__(self, user_id, title, description, category, proficiency="beginner"):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.category = category
        self.proficiency = proficiency
        self.is_verified = False
        self.endorsements = 0

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "proficiency": self.proficiency,
            "is_verified": self.is_verified,
            "endorsements": self.endorsements
        }
