from flask import Blueprint, jsonify
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis, sentiment_analysis_top_comments_by_country
from app.services.db import get_latest_posts_by_subreddit
from app.services.reddit_api import get_posts
from app.helpers.post_util import comments_of_top_posts
import asyncio

bp = Blueprint('posts', __name__, url_prefix='/posts')

# get method for fetching and analyzing Reddit data
# not connected to database
@bp.route('/<subreddit>/<type>/<int:amount>', methods=['GET'])
def get_posts_subreddit(subreddit,type,amount):
    posts = asyncio.run(get_posts(subreddit,type,amount))

    topics = extract_topics(posts)
    analyzed_topics = sentiment_analysis(topics)

    return jsonify(analyzed_topics)


# get method for retrieving most recently analyzed posts for a given subreddit
# connected to database
@bp.route('/latest/<subreddit>', methods=['GET'])
def get_latest_posts_from_db(subreddit):
    data = get_latest_posts_by_subreddit(subreddit)

    if len(data) == 0:
        return jsonify({"error": "No data found for this subreddit"}), 404
    
    return jsonify(data)


@bp.route('/<subreddit>', methods=['GET'])
def get_hot_comments_by_country(subreddit):
    posts = asyncio.run(get_posts(subreddit, "hot", 10))
    comments =  comments_of_top_posts(posts)
    analyzed_comments = sentiment_analysis_top_comments_by_country(comments)
    
    return jsonify(analyzed_comments)



