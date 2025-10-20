import asyncio
from app.services.reddit_api import get_posts
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis
from app.services.db import save_posts_to_database
from app.config import Config

""""
For GitHhub Actions workflow:
Fetches and analyzes posts from the given subreddits, and inserts the results into the database
"""

def pipeline(subreddit):
    print(f"===== PROCESSING SUBREDDIT: {subreddit} =====")
        
    try:
        posts = asyncio.run(get_posts(subreddit, "hot", 500, 2))
    except Exception as e:
        print(f"::error::Error fetching posts: {e}")

    try:
        topics = extract_topics(posts)
    except Exception as e:
        print(f"::error::Error extracting topics: {e}")

    try:
        analyzed_topics = sentiment_analysis(topics)
    except Exception as e:
        print(f"::error::Error analyzing sentiment: {e}")

    try:
        save_posts_to_database(analyzed_topics, subreddit, "posts")
    except Exception as e:
        print(f"::error::Error inserting into database: {e}")
        
    print("Pipeline complete.")

if __name__ == "__main__":
    subreddits = Config.SUBREDDITS

    for subreddit in subreddits:
        try:
            pipeline(subreddit)
        except Exception as e:
            print(f"::error::Pipeline failed for {subreddit}: {e}")