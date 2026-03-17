def calculate_credibility_score(user_id, db):
    """
    Recalculates a user's credibility score based on:
    - GitHub score / Proof quality
    - Peer validation feedback ratings
    - Session completion count
    Updates the user profile.
    """
    try:
        # Base from proofs
        proof = db.proofs.find_one({"user_id": str(user_id), "status": "approved"})
        score = proof.get("github_score", 0) if proof else 0
        
        # Sessions completed (10 points each, up to 100)
        sessions_completed = db.sessions.count_documents({"provider_id": str(user_id), "status": "completed"})
        score += min(sessions_completed * 10, 100)
        
        # Feedback rating average (up to 100 points)
        feedbacks = list(db.feedback.find({"reviewee_id": str(user_id)}))
        if feedbacks:
            avg_rating = sum(float(f["rating"]) for f in feedbacks) / len(feedbacks)
            score += (avg_rating / 5.0) * 100
            
        final_score = int(score)
        
        # Update user
        db.users.update_one(
            {"_id": user_id},
            {"$set": {"credibility_score": final_score}}
        )
        
        return final_score
        
    except Exception as e:
        print(f"Error calculating credibility: {e}")
        return 0
