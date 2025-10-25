from flask import Blueprint, jsonify
from app.services.db import get_latest_posts_by_subreddit

bp = Blueprint('countries', __name__, url_prefix='/countries')

# Get latest batch of analyzed data for a given country subreddit
@bp.route('/latest/<subreddit>', methods=['GET'])
def get_latest_country_data(subreddit):
    data = get_latest_posts_by_subreddit(subreddit, "countries")

    if len(data) == 0:
        return jsonify({"error": "No data found for this subreddit"}), 404
    
    return jsonify(data)