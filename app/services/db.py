from pymongo import MongoClient, DESCENDING
import os

def save_posts_to_database(posts_to_save, collection):
    client = connect_db()
    db = client.reddit
    coll = db[collection]
    coll.insert_many(posts_to_save)
    client.close()

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

    client.close()
    return data