from flask import Blueprint, jsonify
from app.services.db import get_latest_data_by_subreddit


topics_bp = Blueprint('topics', __name__)

# get method for retrieving most recently analyzed posts for a given subreddit
# connected to database
@topics_bp.route('/latest/<subreddit>', methods=['GET'])
def get_latest_posts_from_db(subreddit):
    data = get_latest_data_by_subreddit("posts", subreddit)

    if not data:
        return jsonify({"error": "No data found for this subreddit"}), 404
    
    return jsonify(data)



