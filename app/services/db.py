from datetime import datetime, timezone
from pymongo import MongoClient
import os

def connect_db():
    # Here goes your Mongodb Atlas connection string
    uri = os.getenv("ATLAS_CONNECTION_STR")
    #connects to the database
    client = MongoClient(uri)
    return client

def get_reddit_posts():
    client = connect_db()

    # This creates new database called 'reddit'
    db = client.reddit
    # This creates new collection called 'posts'
    coll = db.posts
    #this gets all the posts from the database
    posts = coll.find()

    #converting data to json format for the api

    list_json = list(posts)

    data = []

    for post in list_json:
        data.append(
            {
                "id": post["id"],
                "title":  post["title"],
                "content":post["content"],
                "comments": post["comments"],
                "num_comments": post["num_comments"],
                "score":  post["score"],
                "upvote_ratio":post["upvote_ratio"]
            }
        )

    return data

# for fetching posts from a given subreddit, assuming the pipeline saves data to the db once per day
def get_latest_posts_by_subreddit(subreddit):
    client = connect_db()

    # start of the day in utc (00:00)
    start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    db = client.reddit
    data = list(db.posts.find({
        "timestamp": {"$gte": start}, # fetches posts that were saved to the db during current day
        "subreddit": subreddit
    }))
    
    for post in data:
        post["_id"] = str(post["_id"])  # convert Mongo ObjectId to string

    client.close()
    return data