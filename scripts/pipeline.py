import os
import asyncio
from app.services.reddit_api import get_posts
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis
from pymongo import MongoClient

# for github actions workflow
def pipeline():
    try:
        posts = asyncio.run(get_posts("technology", "hot", 500))
    except Exception as e:
        print(f"::error::Error fetching posts: {e}")
        return

    try:
        topics = extract_topics(posts)
    except Exception as e:
        print(f"::error::Error extracting topics: {e}")
        return

    try:
        analyzed_topics = sentiment_analysis(topics)
    except Exception as e:
        print(f"::error::Error analyzing sentiment: {e}")
        return

    try:
        # DATABASE TEST
        print("Inserting into database..")
        uri = os.getenv("ATLAS_CONNECTION_STR")
        client = MongoClient(uri)
        db = client.reddit
        coll = db.posts
        coll.drop()
        coll.insert_many(analyzed_topics)
        client.close()
    except Exception as e:
        print(f"::error::Error inserting into database: {e}")

if __name__ == "__main__":
    pipeline()