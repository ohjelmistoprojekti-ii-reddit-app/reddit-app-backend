from flask import Blueprint, jsonify
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis
from app.services.reddit_api import get_posts
import asyncio

reddit_api_bp = Blueprint('posts', __name__, url_prefix='/posts')

# get method for fetching and analyzing Reddit data
# not connected to database
@reddit_api_bp.route('/<subreddit>/<type>/<int:amount>', methods=['GET'])
def get_posts_subreddit(subreddit,type,amount):
    posts = asyncio.run(get_posts(subreddit,type,amount,2))

    topics = extract_topics(posts)
    analyzed_topics = sentiment_analysis(topics)

    return jsonify(analyzed_topics)