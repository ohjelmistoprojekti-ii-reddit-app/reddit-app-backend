class Config:
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
        { "id": "FI", "name": "Finland", "subreddit": "suomi" },
        { "id": "SE", "name": "Sweden", "subreddit": "sweden" },
        { "id": "NO", "name": "Norway", "subreddit": "norway" },
        { "id": "IT", "name": "Italy", "subreddit": "italia" },
        { "id": "ES", "name": "Spain", "subreddit": "spain" },
        { "id": "DE", "name": "Germany", "subreddit": "de" },
        { "id": "PL", "name": "Poland", "subreddit": "polska" },
        { "id": "FR", "name": "France", "subreddit": "france" },
        { "id": "GR", "name": "Greece", "subreddit": "greece" },
        { "id": "PT", "name": "Portugal", "subreddit": "portugal" },
        { "id": "TR", "name": "Turkey", "subreddit": "turkey" },
        { "id": "ZA", "name": "South Africa", "subreddit": "southafrica" },
        { "id": "NG", "name": "Nigeria", "subreddit": "nigeria" },
        { "id": "MX", "name": "Mexico", "subreddit": "mexico" },
        { "id": "IN", "name": "India", "subreddit": "india" },
        { "id": "CA", "name": "Canada", "subreddit": "canada" },
        { "id": "TH", "name": "Thailand", "subreddit": "thailand" },
        { "id": "JP", "name": "Japan", "subreddit": "japan" },
        { "id": "BR", "name": "Brazil", "subreddit": "brazil" },
        { "id": "AU", "name": "Australia", "subreddit": "australia" },
        { "id": "AR", "name": "Argentina", "subreddit": "argentina" },
        { "id": "CN", "name": "China", "subreddit": "china" },
        { "id": "NZ", "name": "New Zealand", "subreddit": "newzealand" },
    ]