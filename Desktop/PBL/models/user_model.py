class User:
    def __init__(self, name, email, password, role="learner"):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.verified = False
        self.credibility_score = 0

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "verified": self.verified,
            "credibility_score": self.credibility_score
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role", "learner")
        )
        user.verified = data.get("verified", False)
        user.credibility_score = data.get("credibility_score", 0)
        return user