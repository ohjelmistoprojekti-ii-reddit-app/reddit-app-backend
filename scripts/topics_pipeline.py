import asyncio
from datetime import datetime, timezone
from external_api.reddit_api import get_posts
from data_processing.topic_modeling import extract_topics
from data_processing.sentiment_analysis import sentiment_analysis
from app.services.db import save_data_to_database
from app.config import Config
import sys

"""
For GitHub Actions workflow:
Fetches and analyzes posts from the given subreddits, and inserts the results into the database

Usage: python -m scripts.topics_pipeline
"""

def topics_pipeline(subreddit):
    print(f"===== PROCESSING SUBREDDIT: {subreddit} =====")
    
    try:
        posts = asyncio.run(get_posts(subreddit, "hot", 500, 2))
        topics = extract_topics(posts)
        analyzed_topics = sentiment_analysis(topics)

        for topic in analyzed_topics:
            topic["subreddit"] = subreddit  # add subreddit info to each topic
            topic["timestamp"] = datetime.now(timezone.utc)  # add timestamp to each topic

        save_data_to_database(analyzed_topics, "posts")
        return True
    except Exception as e:
        print(f"::error::Pipeline failed for '{subreddit}': {e}")
        return False

if __name__ == "__main__":
    subreddits = Config.SUBREDDITS

    failure = False

    for subreddit in subreddits:
        success = topics_pipeline(subreddit)
        if success:
            print(f"✔️  Successfully analyzed '{subreddit}'\n")
        else:
            failure = True

    # Make sure that GitHub Actions workflow fails if any subreddit processing fails
    if failure:
        sys.exit(1)
