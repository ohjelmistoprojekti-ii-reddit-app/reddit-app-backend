from flask import Blueprint, jsonify
from app.models.sentiment_analysis import sentiment_analysis_for_map_feature
from app.services.db import get_latest_posts_by_subreddit
from app.services.reddit_api import get_posts
from app.helpers.post_util import get_top_posts_with_translations
import asyncio

topics_bp = Blueprint('topics', __name__, url_prefix='/topics')

# get method for retrieving most recently analyzed posts for a given subreddit
# connected to database
@topics_bp.route('/latest/<subreddit>', methods=['GET'])
def get_latest_posts_from_db(subreddit):
    data = get_latest_posts_by_subreddit(subreddit, "posts")

    if len(data) == 0:
        return jsonify({"error": "No data found for this subreddit"}), 404
    
    return jsonify(data)


@topics_bp.route('/hot/<subreddit>', methods=['GET'])
def get_hot_comments_by_country(subreddit):
    posts = asyncio.run(get_posts(subreddit, "hot", 10, 4))
    top_posts = asyncio.run(get_top_posts_with_translations(posts))
    analyzed_posts = sentiment_analysis_for_map_feature(top_posts)
    
    return jsonify(analyzed_posts)



