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

    # (Initial) subreddit options for the map feature
    # The country codes and names are needed for the svg map in frontend
    COUNTRY_SUBREDDITS = [
        { "id": "FI", "name": "Finland", "subredditName": "suomi" },
        { "id": "SE", "name": "Sweden", "subredditName": "sweden" },
        { "id": "IT", "name": "Italy", "subredditName": "italia" },
        { "id": "MX", "name": "Mexico", "subredditName": "mexico" },
        { "id": "ES", "name": "Spain", "subredditName": "spain" },
        { "id": "EG", "name": "Egypt", "subredditName": "egypt" },
        { "id": "ZA", "name": "South Africa", "subredditName": "southafrica" },
        { "id": "IN", "name": "India", "subredditName": "india" },
    ]