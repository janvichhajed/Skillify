from datetime import datetime

class Proof:
    def __init__(self, user_id, github_url=None, cert_url=None, portfolio_url=None, demo_video_url=None, category=None):
        self.user_id = user_id
        self.github_url = github_url
        self.cert_url = cert_url
        self.portfolio_url = portfolio_url
        self.demo_video_url = demo_video_url
        self.category = category
        self.status = "pending" # pending, approved, rejected
        self.github_score = 0
        self.submitted_at = datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "github_url": self.github_url,
            "cert_url": self.cert_url,
            "portfolio_url": self.portfolio_url,
            "demo_video_url": self.demo_video_url,
            "category": self.category,
            "status": self.status,
            "github_score": self.github_score,
            "submitted_at": self.submitted_at
        }

    @classmethod
    def from_dict(cls, data):
        proof = cls(
            user_id=data.get("user_id"),
            github_url=data.get("github_url"),
            cert_url=data.get("cert_url"),
            portfolio_url=data.get("portfolio_url"),
            demo_video_url=data.get("demo_video_url"),
            category=data.get("category")
        )
        proof.status = data.get("status", "pending")
        proof.github_score = data.get("github_score", 0)
        proof.submitted_at = data.get("submitted_at")
        return proof
