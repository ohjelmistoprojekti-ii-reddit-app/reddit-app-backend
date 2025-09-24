from flask import Blueprint, jsonify
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis
from app.services.db import get_reddit_posts, get_latest_posts_by_subreddit
from app.services.reddit_api import get_posts
import asyncio

bp = Blueprint('posts', __name__, url_prefix='/posts')

# This GET method gets the posts from reddit api and returns analyzed data
# not connected to database
@bp.route('/<subreddit>/<type_subbreddit>/<int:count>', methods=['GET'])
def get_posts_subreddit(subreddit,type_subbreddit,count):
    posts = asyncio.run(get_posts(subreddit,type_subbreddit,count))

    topics = extract_topics(posts)
    analyzed_topics = sentiment_analysis(topics)

    return jsonify(analyzed_topics)


# get method for fetching latest posts from a given subreddit
# connected to database
@bp.route('/latest/<subreddit>', methods=['GET'])
def get_latest_posts_from_db(subreddit):
    data = get_latest_posts_by_subreddit(subreddit)
    return jsonify(data)

# # get method for sentiment analysis
# @bp.route('/', methods=['GET'])
# def get_reddit_analysis():
#     #gets the data from the database
#     data = get_reddit_posts()

#     topics = extract_topics(data)
#     analyzed_topics = sentiment_analysis(topics)

#     return jsonify(analyzed_topics)

# get method for all posts from the database
# @bp.route('/', methods=['GET'])
# def get_reddit_posts():
#     data = get_reddit_posts()

#     return jsonify(data)


