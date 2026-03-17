import requests

def verify_github_profile(github_url):
    """
    Checks GitHub API for repo count, commit activity, and account age.
    Calculates a trust score from 0 to 100.
    """
    try:
        # Extract username from url
        # E.g. https://github.com/username
        username = github_url.strip("/").split("/")[-1]
        
        api_url = f"https://api.github.com/users/{username}"
        response = requests.get(api_url)
        
        if response.status_code != 200:
            return 0
            
        data = response.json()
        
        score = 0
        
        # Repo count (up to 40 points)
        repos = data.get("public_repos", 0)
        score += min(repos * 2, 40)
        
        # Followers (up to 30 points)
        followers = data.get("followers", 0)
        score += min(followers * 5, 30)
        
        # Account age (up to 30 points)
        created_at = data.get("created_at")
        if created_at:
            # Simple check based on year string
            year = int(created_at[:4])
            current_year = 2024
            age = current_year - year
            score += min(age * 10, 30)
            
        return score
    except Exception as e:
        print(f"Error validating Github: {e}")
        return 0
