from flask import Blueprint, jsonify
from app.config import Config

subbreddits_bp = Blueprint('subreddits', __name__)

# Get list of subreddits that are analyzed daily via our GitHub Actions workflow
# Can be used for filtering categories in frontend
@subbreddits_bp.route('/', methods=['GET'])
def get_subreddits():
    subreddits = Config.SUBREDDITS
    return jsonify(subreddits)

# Get subreddit options for the map feature
@subbreddits_bp.route('/countries', methods=['GET'])
def get_countries():
    country_subreddits = Config.COUNTRY_SUBREDDITS
    return jsonify(country_subreddits)
