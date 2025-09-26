import os
import asyncio
import datetime
from app.services.reddit_api import get_posts
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis
from pymongo import MongoClient

subreddits = [
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

# for github actions workflow
# fetches and analyzes posts from the given subreddits
# and inserts the results into the database
def pipeline(subreddits):
    for subreddit in subreddits:
        print(f"===== PROCESSING SUBREDDIT: {subreddit} =====")
        
        try:
            posts = asyncio.run(get_posts(subreddit, "hot", 500))
        except Exception as e:
            print(f"::error::Error fetching posts: {e}")
            return

        try:
            topics = extract_topics(posts)
        except Exception as e:
            print(f"::error::Error extracting topics: {e}")
            return

        try:
            print("Analyzing sentiment..")
            analyzed_topics = sentiment_analysis(topics)
        except Exception as e:
            print(f"::error::Error analyzing sentiment: {e}")
            return

        try:
            # add subreddit and run timestamp to each topic for easier db filtering
            for topic in analyzed_topics:
                topic["timestamp"] = datetime.datetime.now(datetime.timezone.utc)
                topic["subreddit"] = subreddit

            # DATABASE TEST - will be refactored later
            print("Inserting into database..\n")
            uri = os.getenv("ATLAS_CONNECTION_STR")
            client = MongoClient(uri)
            db = client.reddit
            coll = db.posts
            coll.insert_many(analyzed_topics)
            client.close()
        except Exception as e:
            print(f"::error::Error inserting into database: {e}")

    print("Analysis complete.")

if __name__ == "__main__":
    pipeline(subreddits)