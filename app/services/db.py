from pymongo import MongoClient, DESCENDING
from datetime import datetime, timedelta, timezone
import os

def connect_db():
    uri = os.getenv("ATLAS_CONNECTION_STR")
    client = MongoClient(uri)
    return client

def save_posts_to_database(posts_to_save, collection):
    print("Inserting into database..\n")
    client = connect_db()
    db = client.reddit
    coll = db[collection]
    coll.insert_many(posts_to_save)
    client.close()

# get most recently analyzed data for a given subreddit
def get_latest_posts_by_subreddit(subreddit):
    client = connect_db()
    db = client.reddit

    latest_entry = db.posts.find_one(
        {"subreddit": subreddit},
        sort=[("timestamp", DESCENDING)]
    )

    if latest_entry is None:
        return []

    latest_timestamp = latest_entry["timestamp"]

    # get all posts with the most recent timestamp for a given subreddit
    data = list(db.posts.find({
        "timestamp": latest_timestamp,
        "subreddit": subreddit
    }))
    
    for post in data:
        post["_id"] = str(post["_id"])  # convert Mongo ObjectId to string

    sorted_data = sorted(data, key=lambda k: k['topic_id'])

    client.close()
    return sorted_data

def get_post_numbers_by_timeperiod(subreddit, number_of_days):
    client = connect_db()
    db = client.reddit
    collection = db["posts"]

    date_today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    min_date = date_today - timedelta(days=number_of_days)
    max_date = date_today

    # build aggregation pipeline 
    pipeline = [
        # match with timestamp >= min_date
        {"$match": {
            "subreddit": subreddit,
            "timestamp": {"$gte": min_date, "$lt": max_date}
        }},

        # pass docs to next stage in the pipeline
        {"$project": {
            "num_posts": 1,
            "day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}}
        }},

        # group by day to get num_posts per day
        {"$group": {
            "_id": "$day",
            "posts_per_day": {"$sum": "$num_posts"}
        }},
        {"$sort": {"_id": 1}},

        #group by subreddit to push posts per day and total posts
        {"$group": {
            "_id": subreddit,
            "total_posts": {"$sum": "$posts_per_day"},
            "daily": {
                "$push": {
                    "day": "$_id",
                    "posts": "$posts_per_day"
                }
            }
        }},

    ]

    post_numbers = list(collection.aggregate(pipeline))
    client.close()
    
    return post_numbers