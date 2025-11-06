from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.sentiment_analysis import sentiment_analysis_for_map_feature
from app.services.db import get_latest_data_by_subreddit
from app.services.reddit_api import get_posts
from app.helpers.post_util import get_top_posts_with_translations
from app.helpers.jwt_utils import is_token_revoked
import asyncio
from app.config import Config

topics_bp = Blueprint('topics', __name__)

# get method for retrieving most recently analyzed posts for a given subreddit
# connected to database
@topics_bp.route('/latest/<subreddit>', methods=['GET'])
def get_latest_posts_from_db(subreddit):
    data = get_latest_data_by_subreddit("posts", subreddit)

    if not data:
        return jsonify({"error": "No data found for this subreddit"}), 404
    
    return jsonify(data)


# @topics_bp.route('/hot/<subreddit>', methods=['GET'])
# def get_hot_comments_by_country(subreddit):
#     posts = asyncio.run(get_posts(subreddit, "hot", 10, 4))
#     top_posts = asyncio.run(get_top_posts_with_translations(posts))
#     analyzed_posts = sentiment_analysis_for_map_feature(top_posts)
    
#     return jsonify(analyzed_posts)

# @topics_bp.route('/hot/<subreddit>', methods=['GET'])
# @jwt_required(optional=True)
# def get_hot_comments_by_country(subreddit):
#     country = None
#     for c in Config.COUNTRY_SUBREDDITS:
#         if c["subreddit"].lower() == subreddit.lower():
#             country = c
#             break

#     if not country:
#         return jsonify({"error": "Subreddit not found"}), 404
    
#     current_user = get_jwt_identity()

#     if current_user and country.get("login_required"):
#         if is_token_revoked():
#             return jsonify({"msg": "Token revoked"}), 401

#     if country.get("login_required") and not current_user:
#         return jsonify({"error": "Login required to access this subreddit"}), 401
    
#     posts = asyncio.run(get_posts(subreddit, "hot", 10, 4))
#     top_posts = asyncio.run(get_top_posts_with_translations(posts))
#     analyzed_posts = sentiment_analysis_for_map_feature(top_posts)
    
#     return jsonify({
#         "country": country["name"],
#         "requiresLogin": bool(country["login_required"]),
#         "requestedBy": current_user or "anonymous",
#         "posts": analyzed_posts
#     })


