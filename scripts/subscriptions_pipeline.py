import asyncio
from datetime import datetime, timezone
from app.services.reddit_api import get_posts
from scripts.topic_modeling import extract_topics
from scripts.sentiment_analysis import sentiment_analysis, sentiment_analysis_for_posts
from app.services.db import fetch_data_from_collection, save_data_to_database
import sys

"""
For GitHub Actions workflow:
Fetches and analyzes posts from the subreddits with active subscriptions, and inserts the results into the database

Usage: python -m scripts.subscriptions_pipeline --posts | --topics
"""

def subscriptions_pipeline(subreddit, amount_of_posts, topics):
    print(f"===== PROCESSING SUBREDDIT: {subreddit} =====")
    
    try:
        posts = asyncio.run(get_posts(subreddit, "hot", amount_of_posts, 2))
        
        if topics:
            extracted_topics = extract_topics(posts)
            results = sentiment_analysis(extracted_topics)
        else:
            analyzed_data = sentiment_analysis_for_posts(posts)
            results = [{"posts": analyzed_data}]

        for item in results:
            item["subreddit"] = subreddit  # add subreddit info to each item
            item["timestamp"] = datetime.now(timezone.utc)  # add timestamp to each item
            item["type"] = "topics" if topics else "posts" # add analysis type info to each item

        save_data_to_database(results, "subscriptions_data")
        return True
    except Exception as e:
        print(f"::error::Pipeline failed for '{subreddit}': {e}")
        return False

if __name__ == "__main__":
    # Fetch active subscriptions from the database based on analysis type
    if '--posts' in sys.argv:
        subscriptions = fetch_data_from_collection("subscriptions", {"analysis_type": "posts", "active": True})
        amount_of_posts = 10
        analyze_topics = False

        if not subscriptions:
            print("No active subscriptions found for posts analysis.")
            sys.exit(0)
    elif '--topics' in sys.argv:
        subscriptions = fetch_data_from_collection("subscriptions", {"analysis_type": "topics", "active": True})
        amount_of_posts = 500
        analyze_topics = True

        if not subscriptions:
            print("No active subscriptions found for topics analysis.")
            sys.exit(0)
    else:
        print("::error::Please specify either --posts or --topics as an argument.")
        sys.exit(1)

    failure = False

    for subscription in subscriptions:
        subreddit = subscription['subreddit']
        success = subscriptions_pipeline(subreddit, amount_of_posts, topics=analyze_topics)
        if success:
            print(f"✔️  Successfully analyzed '{subreddit}'\n")
        else:
            failure = True

    # Make sure that GitHub Actions workflow fails if any subreddit processing fails
    if failure:
        sys.exit(1)