
from pymongo import MongoClient
import os

def get_reddit_posts():
    # Here goes your Mongodb Atlas connection string
    uri = os.getenv("ATLAS_CONNECTION_STR")
    #connects to the database
    client = MongoClient(uri)
    # This creates new database called 'reddit'
    db = client.reddit
    # This creates new collection called 'posts'
    coll = db.posts
    #this gets all the posts from the database
    posts = coll.find()

    #converting data to json format

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



    