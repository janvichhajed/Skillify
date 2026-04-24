def calculate_credibility_score(user_id, db):
    """
    Recalculates a user's credibility score strictly out of 10 based on session feedback.
    """
    try:
        from bson import ObjectId
        uid_obj = ObjectId(user_id) if len(str(user_id)) == 24 else user_id

        feedbacks = list(db.feedback.find({"reviewee_id": str(user_id)}))
        
        if not feedbacks:
            # Starter score based on verification status
            user_doc = db.users.find_one({"_id": uid_obj})
            if user_doc and user_doc.get("verification_status") == "Approved":
                final_score = 7.0
            else:
                final_score = 0.0
        else:
            # Exactly OUT OF 10 from feedback averages
            avg_rating = sum(float(f["rating"]) for f in feedbacks) / len(feedbacks)
            
            # Small bonus for high volume of sessions (+0.1 per session up to 1.0 max)
            sessions_completed = db.sessions.count_documents({"provider_id": str(user_id), "status": "completed"})
            bonus = min(sessions_completed * 0.1, 1.0)
            
            final_score = min(round(avg_rating + bonus, 1), 10.0)
            
        # Update user
        db.users.update_one(
            {"_id": uid_obj},
            {"$set": {"credibility_score": final_score}}
        )
        
        return final_score
        
    except Exception as e:
        print(f"Error calculating credibility: {e}")
        return 0
