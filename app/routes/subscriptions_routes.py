import asyncio
from datetime import datetime, timezone
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.helpers.auth_utils import get_current_user_id, convert_userids_to_string
from app.helpers.jwt_utils import is_token_revoked
from app.services.db import fetch_collection_data, get_latest_data_by_subreddit, save_data_to_database, update_collection_data
from app.services.reddit_api import get_posts

bp = Blueprint('subscriptions', __name__, url_prefix='/subscriptions')


# Get list of active subscriptions by analysis type
@bp.route('/type/<type>', methods=['GET'])
def fetch_subscriptions_by_type(type):
    subscriptions = fetch_collection_data("subscriptions", {"analysis_type": type, "active": True})

    if not subscriptions:
        return jsonify({"error": "No active subscriptions"}), 404

    subscriptions = convert_userids_to_string(subscriptions)
    return jsonify(subscriptions)


# Get subscriptions for the current user
@bp.route('/current-user', methods=['GET'])
@jwt_required()
def fetch_current_user_subscriptions():
    try:
        current_user_id = get_current_user_id()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    if is_token_revoked():
        return jsonify({"msg": "Token revoked"}), 401

    subscriptions = fetch_collection_data("subscriptions", {"subscribers": current_user_id})

    if not subscriptions:
        return jsonify({"error": "No active subscriptions for this user"}), 404
    
    subscriptions = convert_userids_to_string(subscriptions)
    return jsonify(subscriptions)


# Add new subscription for current user
# If subreddit already has active subscriptions, add current user to subscribers list. Otherwise create a new subscription.
@bp.route('/current-user/add/<subreddit>/<type>', methods=['POST'])
@jwt_required()
def add_subscription(subreddit, type):
    try:
        current_user_id = get_current_user_id()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    if is_token_revoked():
        return jsonify({"msg": "Token revoked"}), 401

    if type not in ["posts", "topics"]:
        return jsonify({"error": "Analysis type must be 'posts' or 'topics'"}), 400

    existing_subscriptions_for_current_user = fetch_collection_data("subscriptions", {"subscribers": current_user_id})

    # Limit max subscriptions to 1 per user for now
    if len(existing_subscriptions_for_current_user) >= 1:
        return jsonify({"error": "User has reached the maximum number of active subscriptions"}), 400

    # Check for existing active subscriptions to the same subreddit
    existing_subscriptions_for_subreddit = fetch_collection_data(
        "subscriptions",
        {"subreddit": subreddit, "analysis_type": type, "active": True}
    )

    # If subreddit already has active subscriptions, add current user to subscribers list
    if existing_subscriptions_for_subreddit:
        try:
            update_collection_data(
                "subscriptions",
                {"subreddit": subreddit, "analysis_type": type, "active": True},
                {"$addToSet": {"subscribers": current_user_id}}
            )
            return jsonify({"message": f"User added to existing subscription"}), 200
        except Exception as e:
            return jsonify({"error": "Failed to add user to existing subscription", "details": str(e)}), 500

    # If subreddit has no active subscriptions, create a new subscription
    else:
        # Check that subreddit exists by fetching 1 post
        try:
            asyncio.run(get_posts(subreddit, "hot", 1, 6))
        except Exception as e:
            return jsonify({"error": "Subreddit not found", "details": str(e)}), 404

        subscription = {
            "subreddit": subreddit,
            "analysis_type": type,
            "subscribers": [current_user_id],
            "active": True,
            "created_at": datetime.now(timezone.utc),
        }

        try:
            # Save new subscription
            save_data_to_database(subscription, "subscriptions")
            return jsonify({"message": f"New subscription created for current user"}), 201
        except Exception as e:
            return jsonify({"error": "Failed to add new subscription", "details": str(e)}), 500


# Deactivate current subscription
@bp.route('/current-user/deactivate', methods=['PATCH'])
@jwt_required()
def deactivate_current_subscription():
    try:
        current_user_id = get_current_user_id()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    if is_token_revoked():
        return jsonify({"msg": "Token revoked"}), 401
    
    # Get users active subscriptions
    active_subscriptions = fetch_collection_data("subscriptions", {"subscribers": current_user_id})

    if not active_subscriptions:
        return jsonify({"error": "No active subscription found for this user"}), 404

    subreddit = active_subscriptions[0]["subreddit"]
    analysis_type = active_subscriptions[0]["analysis_type"]

    try:
        # Remove user from subscribers list
        update_collection_data(
            "subscriptions",
            {"subreddit": subreddit, "analysis_type": analysis_type, "active": True},
            {"$pull": {"subscribers": current_user_id}}
        )

        set_to_inactive = False

        # Check if subscribers list is empty, and set subscription to inactive if it is
        updated_subscription = fetch_collection_data(
            "subscriptions",
            {"subreddit": subreddit, "analysis_type": analysis_type, "active": True}
        )

        if len(updated_subscription[0]["subscribers"]) == 0:
            update_collection_data(
                "subscriptions",
                {"subreddit": subreddit, "analysis_type": analysis_type, "active": True},
                {"$set": {"active": False}}
            )
            set_to_inactive = True

        if set_to_inactive:
            return jsonify({"message": f"User removed from subscription to subreddit '{subreddit}'. No more subscribers left, so this subreddit is now inactive."}), 200
        else:
            return jsonify({"message": f"User removed from subscription to subreddit '{subreddit}'"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to update subscription", "details": str(e)}), 500


# Get latest analyzed data for current user's active subscription
@bp.route('/current-user/latest-analyzed', methods=['GET'])
@jwt_required()
def get_latest_analyzed_subscription_data_for_current_user():
    try:
        current_user_id = get_current_user_id()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    if is_token_revoked():
        return jsonify({"msg": "Token revoked"}), 401

    active_subscriptions = fetch_collection_data("subscriptions", {"subscribers": current_user_id})

    if not active_subscriptions:
        return jsonify({"error": "No active subscriptions found for this user"}), 404

    subreddit = active_subscriptions[0]["subreddit"]
    type = active_subscriptions[0]["analysis_type"]
    data = get_latest_data_by_subreddit("subscriptions_data", subreddit, type)

    if not data:
        return jsonify({"error": "No analyzed data found for this subreddit"}), 404
    
    organized_data = {
        "type": type,
        "data": data
    }

    return jsonify(organized_data)