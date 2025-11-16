from pymongo import MongoClient, DESCENDING
from datetime import datetime, timedelta, timezone
import os

def connect_db():
    try:
        uri = os.getenv("ATLAS_CONNECTION_STR")
        if not uri:
            raise ValueError("ATLAS_CONNECTION_STR is not set")
        
        client = MongoClient(uri)
        db = client.reddit
        return client, db
    except Exception as e:
        raise ConnectionError(f"Could not connect to database: {e}")


""" Save data (list or dict) to specified collection """
def save_data_to_database(data_to_save, collection):
    print("Inserting into database..\n")
    if not isinstance(data_to_save, (list, dict)):
        raise TypeError("Data to save must be a list or a dictionary")

    client, db = connect_db()
    coll = db[collection]
    try:
        if isinstance(data_to_save, list):
            coll.insert_many(data_to_save)
        elif isinstance(data_to_save, dict):
            coll.insert_one(data_to_save)
    except Exception as e:
        raise ConnectionError(f"Database error: {e}")
    finally:
        client.close()


"""
Get data from collection based on filter dict
Example usage: fetch_data_from_collection("example_collection", {"id": 123}) -> returns all documents with id 123

If no filter is provided, returns all data in the collection
"""
def fetch_data_from_collection(collection, filter=None):
    if filter is not None and not isinstance(filter, dict):
        raise TypeError("Parameter 'filter' must be a dictionary or None")
    
    client, db = connect_db()
    try:
        coll = db[collection]
        data = list(coll.find(filter or {}))
        if not data:
            return []

        for item in data:
            item["_id"] = str(item["_id"])  # convert Mongo ObjectId to string
        return data
    except Exception as e:
        raise ConnectionError(f"Database error: {e}")
    finally:
        client.close()


"""
Update data in collection based on filter and update dict
Example usage: update_one_item_in_collection("example_collection", {"id": 123}, {"$set": {"active": False}})
-> updates all documents with id 123, setting their 'active' field to False
"""
def update_one_item_in_collection(collection, filter, update):
    if not isinstance(filter, dict):
        raise TypeError("Parameter 'filter' must be a dictionary")
    if not isinstance(update, dict):
        raise TypeError("Parameter 'update' must be a dictionary")
    
    print("Updating data in database..")
    client, db = connect_db()
    try:
        coll = db[collection]
        result = coll.update_one(filter, update)
        if result.matched_count == 0:
            raise ValueError("Update failed: no matching documents found")
    except Exception as e:
        raise ConnectionError(f"Database error: {e}")
    finally:
        client.close()

"""
Delete a single item from a collection based on a filter dict.
Example usage: delete_one_item_from_collection("users", {"_id": ObjectId(user_id)})
→ deletes the user document with the given _id (if it exists).

Returns: deleted_count (int): 1 if a document was deleted and 0 if no matching document was found.
"""
def delete_one_item_from_collection(collection, filter):
    if not isinstance(filter, dict):
        raise TypeError("Parameter 'filter' must be a dictionary")

    client, db = connect_db()
    try:
        coll = db[collection]
        result = coll.delete_one(filter)

        # Return the number of deleted documents for checking
        return result.deleted_count

    except Exception as e:
        raise ConnectionError(f"Database error: {e}")

    finally:
        client.close()        


""" Get most recently added data for a given subreddit """
def get_latest_data_by_subreddit(collection, subreddit, type=None):
    if type is not None and type not in ["posts", "topics"]:
        raise ValueError("Parameter 'type' must be either 'posts', 'topics', or None")

    client, db = connect_db()
    
    try:
        coll = db[collection]
        latest_entry = coll.find_one({"subreddit": subreddit}, sort=[("timestamp", DESCENDING)])

        if not latest_entry:
            return []

        latest_timestamp = latest_entry["timestamp"]
        query = {"subreddit": subreddit, "timestamp": latest_timestamp}
        if type:
            query["type"] = type

        data = list(coll.find(query))

        for post in data:
            post["_id"] = str(post["_id"])  # convert Mongo ObjectId to string

        if data and 'topic_id' in data[0]:
            return sorted(data, key=lambda k: k['topic_id'])
        return data
    finally:
        client.close()


# get daily post numbers and total number of posts for a subreddit in a given timeperiod
def get_post_numbers_by_timeperiod(subreddit, number_of_days):
    client, db = connect_db()
    collection = db["posts"]

    date_today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    min_date = date_today - timedelta(days=number_of_days)
    max_date = date_today

    # build aggregation pipeline
    pipeline = [
        # match with subreddit and timestamp >= min_date
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


# get limit number of top topics and their frequency count for a subreddit in a given timeperiod
def get_top_topics_by_timeperiod(subreddit, number_of_days, limit):
    client, db = connect_db()
    collection = db["posts"]

    date_today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    min_date = date_today - timedelta(days=number_of_days)
    max_date = date_today

    # build aggregation pipeline
    pipeline = [
        # match with subreddit and timestamp >= min_date
        {"$match": {
            "subreddit": subreddit,
            "timestamp": {"$gte": min_date, "$lt": max_date}
        }},

        # unwind array into individual topic docs
        {"$unwind": "$topic"},

        # group by topic to get topic count
        {"$group": {
            "_id": "$topic",
            "count": {"$sum": 1}
        }},

        # sort descending
        {"$sort": {"count": -1}}, 

        # limit number of topics returned
        {"$limit": limit},

        # group by subreddit and push topic and topic count
        {"$group": {
            "_id": subreddit,
            "topics": {"$push": {
                "topic": "$_id",
                "count": "$count"
            }}
        }}
    ]

    topics_list = list(collection.aggregate(pipeline))
    client.close()

    return topics_list
