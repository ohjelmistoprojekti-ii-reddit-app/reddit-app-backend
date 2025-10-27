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
        { "id": "FI", "name": "Finland", "subreddit": "suomi", "loginRequired": 0 },
        { "id": "SE", "name": "Sweden", "subreddit": "sweden", "loginRequired": 0 },
        { "id": "IT", "name": "Italy", "subreddit": "italia", "loginRequired": 0 },
        { "id": "ES", "name": "Spain", "subreddit": "spain", "loginRequired": 0 },
        { "id": "DE", "name": "Germany", "subreddit": "de", "loginRequired": 1 },
        { "id": "PL", "name": "Poland", "subreddit": "polska", "loginRequired": 1 },
        { "id": "FR", "name": "France", "subreddit": "france", "loginRequired": 1 },
        { "id": "ZA", "name": "South Africa", "subreddit": "southafrica", "loginRequired": 1 },
        { "id": "NG", "name": "Nigeria", "subreddit": "nigeria", "loginRequired": 1 },
        { "id": "MX", "name": "Mexico", "subreddit": "mexico", "loginRequired": 0 },
        { "id": "IN", "name": "India", "subreddit": "india", "loginRequired": 1 },
        { "id": "CA", "name": "Canada", "subreddit": "canada", "loginRequired": 1 },
        { "id": "TH", "name": "Thailand", "subreddit": "thailand", "loginRequired": 1 },
        { "id": "JP", "name": "Japan", "subreddit": "japan", "loginRequired": 1 },
        { "id": "BR", "name": "Brazil", "subreddit": "brazil", "loginRequired": 1 },
        { "id": "KR", "name": "South Korea", "subreddit": "korea", "loginRequired": 1 },
        { "id": "AU", "name": "Australia", "subreddit": "australia", "loginRequired": 1 },
        { "id": "AR", "name": "Argentina", "subreddit": "argentina", "loginRequired": 1 },
        { "id": "CN", "name": "China", "subreddit": "china", "loginRequired": 1 },
    ]