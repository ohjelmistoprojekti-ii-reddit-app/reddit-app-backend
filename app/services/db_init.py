from pymongo import MongoClient
from app.services.reddit_api import get_posts
import asyncio
import os

#automatically populate database with reddit posts
# when running the app
def populate_database_reddit_posts():
    # gets the posts from the reddit api
    posts = asyncio.run(get_posts("all", "hot", 500))
    # Here goes your Mongodb Atlas connection string
    uri = os.getenv("ATLAS_CONNECTION_STR")
    client = MongoClient(uri)
    # database and collection code goes here
    # This creates new database called 'reddit'
    db = client.reddit
    # This creates new collection called 'posts'
    coll = db.posts
    coll.drop()
    #this inserts all the posts to the database
    coll.insert_many(posts)
    # Close the connection to MongoDB when you're done.
    client.close()