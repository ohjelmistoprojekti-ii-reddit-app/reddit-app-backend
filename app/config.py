from datetime import timedelta

class Config:
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    
    # What is this key for? Remove if not necessary
    SECRET_KEY = 'your-secret-key'

    # Subreddits that are analyzed daily via our GitHub Actions workflow
    # Also used for filtering categories in frontend
    SUBREDDITS = [
        "worldnews",
        "technology",
        "entertainment",
        "movies",
        "gaming",
        "sports",
        "travel",
        "jobs",
        "futurology",
        "programming",
    ]

    # Country subreddits that are analyzed daily via our GitHub Actions workflow
    # For frontend map feature
    COUNTRY_SUBREDDITS = [
        { "id": "FI", "name": "Finland", "subreddit": "suomi", "login_required": 0 },
        { "id": "SE", "name": "Sweden", "subreddit": "sweden", "login_required": 0 },
        { "id": "IT", "name": "Italy", "subreddit": "italia", "login_required": 0 },
        { "id": "ES", "name": "Spain", "subreddit": "spain", "login_required": 0 },
        { "id": "DE", "name": "Germany", "subreddit": "de", "login_required": 1 },
        { "id": "PL", "name": "Poland", "subreddit": "polska", "login_required": 1 },
        { "id": "FR", "name": "France", "subreddit": "france", "login_required": 1 },
        { "id": "ZA", "name": "South Africa", "subreddit": "southafrica", "login_required": 1 },
        { "id": "NG", "name": "Nigeria", "subreddit": "nigeria", "login_required": 1 },
        { "id": "MX", "name": "Mexico", "subreddit": "mexico", "login_required": 0 },
        { "id": "IN", "name": "India", "subreddit": "india", "login_required": 1 },
        { "id": "CA", "name": "Canada", "subreddit": "canada", "login_required": 1 },
        { "id": "TH", "name": "Thailand", "subreddit": "thailand", "login_required": 1 },
        { "id": "JP", "name": "Japan", "subreddit": "japan", "login_required": 1 },
        { "id": "BR", "name": "Brazil", "subreddit": "brazil", "login_required": 1 },
        { "id": "KR", "name": "South Korea", "subreddit": "korea", "login_required": 1 },
        { "id": "AU", "name": "Australia", "subreddit": "australia", "login_required": 1 },
        { "id": "AR", "name": "Argentina", "subreddit": "argentina", "login_required": 1 },
        { "id": "CN", "name": "China", "subreddit": "china", "login_required": 1 },
    ]