from flask import Blueprint, jsonify
from app.services.reddit_api import get_posts
import asyncio
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis

bp = Blueprint('posts', __name__, url_prefix='/posts')


# This GET method gets the posts from reddit api and returns analyzed data
@bp.route('/<subreddit>/<type_subbreddit>/<int:count>', methods=['GET'])
def get_posts_subreddit(subreddit,type_subbreddit,count):
    posts = asyncio.run(get_posts(subreddit,type_subbreddit,count))

    topics = extract_topics(posts)
    analyzed_topics = sentiment_analysis(topics)

    return jsonify(analyzed_topics)