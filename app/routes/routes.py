from flask import Blueprint, jsonify
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis
from app.services.db import get_reddit_posts

bp = Blueprint('posts', __name__, url_prefix='/posts')


# get method for sentiment analysis
@bp.route('/', methods=['GET'])
def get_reddit_analysis():
    #gets the data from the database
    data = get_reddit_posts()

    topics = extract_topics(data)
    analyzed_topics = sentiment_analysis(topics)

    return jsonify(analyzed_topics)

# get method for all posts from the database
# @bp.route('/', methods=['GET'])
# def get_reddit_posts():
#     data = get_reddit_posts()

#     return jsonify(data)


# This GET method gets the posts from reddit api and returns analyzed data
# @bp.route('/<subreddit>/<type_subbreddit>/<int:count>', methods=['GET'])
# def get_posts_subreddit(subreddit,type_subbreddit,count):
#     posts = asyncio.run(get_posts(subreddit,type_subbreddit,count))

#     topics = extract_topics(posts)
#     analyzed_topics = sentiment_analysis(topics)

#     return jsonify(analyzed_topics)
