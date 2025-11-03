from flask import Blueprint, jsonify
from app.services.db import get_latest_data_by_subreddit
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.helpers.jwt_utils import is_token_revoked
from app.config import Config

countries_bp = Blueprint('countries', __name__, url_prefix='/countries')

# Get latest batch of analyzed data for a given country subreddit
@countries_bp.route('/latest/<subreddit>', methods=['GET'])
@jwt_required(optional=True)
def get_latest_country_data(subreddit):

    current_user = get_jwt_identity()

    country = None
    for c in Config.COUNTRY_SUBREDDITS:
        if c["subreddit"].lower() == subreddit.lower():
            country = c
            break

    if not country:
        return jsonify({"error": "Subreddit not found"}), 404
    
    if current_user and country.get("login_required"):
        if is_token_revoked():
            return jsonify({"msg": "Token revoked"}), 401
    
    if country.get("login_required") and not current_user:
        return jsonify({"error": "Login required to access this subreddit"}), 401

    data = get_latest_data_by_subreddit("countries", subreddit)
    if not data:
        return jsonify({"error": "No data found for this subreddit"}), 404
    
    return jsonify({
        "country": country["name"],
        "requiresLogin": bool(country["login_required"]),
        "requestedBy": current_user or "anonymous",
        "posts": data
    })