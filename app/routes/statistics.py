from flask import Blueprint, jsonify
from app.services.db import get_post_numbers_by_timeperiod, get_top_topics_by_timeperiod


statistics_bp = Blueprint('statistics', __name__)



# get method for retrieving post numbers over x days for a given subreddit
# connected to database
@statistics_bp.route('/<subreddit>/<int:days>', methods=['GET'])
def get_post_numbers_from_db(subreddit, days):
    data = get_post_numbers_by_timeperiod(subreddit, days)

    if len(data) == 0:
        return jsonify({"error": "No data found for this subreddit"}), 404
    
    return jsonify(data)

# get method for retrieving limit number of top topics and their frequency count over x days for a given subreddit
# connected to database
@statistics_bp.route('/topics/<subreddit>/<int:days>/<int:limit>', methods=['GET'])
def get_top_topics_from_db(subreddit, days, limit):
    data = get_top_topics_by_timeperiod(subreddit, days, limit)

    if len(data) == 0:
        return jsonify({"error": "No data found for this subreddit"}), 404
    
    return jsonify(data)



