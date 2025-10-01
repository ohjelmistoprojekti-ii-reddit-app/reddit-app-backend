from pymongo import MongoClient, DESCENDING
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