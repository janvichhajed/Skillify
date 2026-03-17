from datetime import datetime

class Feedback:
    def __init__(self, session_id, reviewer_id, reviewee_id, rating, review_text):
        self.session_id = session_id
        self.reviewer_id = reviewer_id
        self.reviewee_id = reviewee_id
        self.rating = rating # 1 to 5
        self.review_text = review_text
        self.submitted_at = datetime.utcnow()

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "reviewer_id": self.reviewer_id,
            "reviewee_id": self.reviewee_id,
            "rating": self.rating,
            "review_text": self.review_text,
            "submitted_at": self.submitted_at
        }

    @classmethod
    def from_dict(cls, data):
        feedback = cls(
            session_id=data.get("session_id"),
            reviewer_id=data.get("reviewer_id"),
            reviewee_id=data.get("reviewee_id"),
            rating=data.get("rating"),
            review_text=data.get("review_text")
        )
        feedback.submitted_at = data.get("submitted_at")
        return feedback
