import asyncio
from datetime import datetime, timezone
from flask import Blueprint, jsonify
from app.services.db import get_data_from_db_collection, get_latest_data_by_subreddit, save_data_to_database, update_data_in_db_collection
from app.services.reddit_api import get_posts

bp = Blueprint('subscriptions', __name__, url_prefix='/subscriptions')

# Get subscriptions by user ID
@bp.route('/user/<int:user_id>', methods=['GET'])
def fetch_user_subscriptions(user_id):
    subscriptions = get_data_from_db_collection("subscriptions", {"subscribers": user_id})

    if not subscriptions:
        return jsonify({"error": "No active subscriptions for this user"}), 404
    
    return jsonify(subscriptions)


# Get list of active subscriptions by analysis type
@bp.route('/type/<type>', methods=['GET'])
def fetch_subscriptions_by_type(type):
    subscriptions = get_data_from_db_collection("subscriptions", {"analysis_type": type, "active": True})

    if not subscriptions:
        return jsonify({"error": "No active subscriptions"}), 404

    return jsonify(subscriptions)


# Get subscriptions for the current user
@bp.route('/current-user', methods=['GET'])
def fetch_current_user_subscriptions():
    currentuser_id = 222  # TODO: get from auth system
    subscriptions = get_data_from_db_collection("subscriptions", {"subscribers": currentuser_id})

    if not subscriptions:
        return jsonify({"error": "No active subscriptions for this user"}), 404
    
    return jsonify(subscriptions)


# Add new subscription for current user
# If subreddit already has active subscriptions, add current user to subscribers list. Otherwise create a new subscription.
@bp.route('/current-user/add/<subreddit>/<type>', methods=['POST'])
def add_subscription(subreddit, type):
    currentuser_id = 222 # TODO: get from auth system

    if type not in ["posts", "topics"]:
        return jsonify({"error": "Analysis type must be 'posts' or 'topics'"}), 400

    existing_subscriptions_for_current_user = get_data_from_db_collection("subscriptions", {"subscribers": currentuser_id})

    # Limit max subscriptions to 1 per user for now
    if len(existing_subscriptions_for_current_user) >= 1:
        return jsonify({"error": "User has reached the maximum number of active subscriptions"}), 400

    # Check for existing active subscriptions to the same subreddit
    existing_subscriptions_for_subreddit = get_data_from_db_collection(
        "subscriptions",
        {"subreddit": subreddit, "analysis_type": type, "active": True}
    )

    # If subreddit already has active subscriptions, add current user to subscribers list
    if existing_subscriptions_for_subreddit:
        try:
            update_data_in_db_collection(
                "subscriptions",
                {"subreddit": subreddit, "analysis_type": type, "active": True},
                {"$addToSet": {"subscribers": currentuser_id}}
            )
            return jsonify({"message": f"User {currentuser_id} added to existing subscription"}), 200
        except Exception as e:
            return jsonify({"error": "Failed to add user to existing subscription", "details": str(e)}), 500

    # If subreddit has no active subscriptions, create a new subscription
    else:
        # Check that subreddit exists by fetching 1 post
        try:
            asyncio.run(get_posts(subreddit, "hot", 1, 6))
        except Exception as e:
            return jsonify({"error": "Subreddit not found", "details": str(e)}), 400

        subscription = {
            "subreddit": subreddit,
            "analysis_type": type,
            "subscribers": [currentuser_id],
            "active": True,
            "created_at": datetime.now(timezone.utc),
        }

        try:
            # Save new subscription
            save_data_to_database(subscription, "subscriptions")
            return jsonify({"message": f"New subscription created for user {currentuser_id}"}), 201
        except Exception as e:
            return jsonify({"error": "Failed to add new subscription", "details": str(e)}), 500


# Deactivate current subscription
@bp.route('/current-user/deactivate', methods=['PATCH'])
def deactivate_current_subscription():
    currentuser_id = 222  # TODO: get from auth system

    # Get users active subscriptions
    active_subscriptions = get_data_from_db_collection("subscriptions", {"subscribers": currentuser_id})

    if not active_subscriptions:
        return jsonify({"error": "No active subscription found for this user"}), 404

    subreddit = active_subscriptions[0]["subreddit"]
    analysis_type = active_subscriptions[0]["analysis_type"]

    try:
        # Remove user from subscribers list
        update_data_in_db_collection(
            "subscriptions",
            {"subreddit": subreddit, "analysis_type": analysis_type, "active": True},
            {"$pull": {"subscribers": currentuser_id}}
        )

        set_to_inactive = False

        # Check if subscribers list is empty, and set subscription to inactive if it is
        updated_subscription = get_data_from_db_collection(
            "subscriptions",
            {"subreddit": subreddit, "analysis_type": analysis_type, "active": True}
        )

        if len(updated_subscription[0]["subscribers"]) == 0:
            update_data_in_db_collection(
                "subscriptions",
                {"subreddit": subreddit, "analysis_type": analysis_type, "active": True},
                {"$set": {"active": False}}
            )
            set_to_inactive = True

        if set_to_inactive:
            return jsonify({"message": f"User {currentuser_id} removed from subscription to subreddit '{subreddit}'. No more subscribers left, so this subreddit is now inactive."}), 200
        else:
            return jsonify({"message": f"User {currentuser_id} removed from subscription to subreddit '{subreddit}'"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to update subscription", "details": str(e)}), 500


# Get latest analyzed data for current user's active subscription
@bp.route('/current-user/latest-analyzed', methods=['GET'])
def get_latest_analyzed_subscription_data_for_current_user():
    currentuser_id = 222  # TODO: get from auth system
    active_subscriptions = get_data_from_db_collection("subscriptions", {"subscribers": currentuser_id})

    if not active_subscriptions:
        return jsonify({"error": "No active subscriptions found for this user"}), 404

    subreddit = active_subscriptions[0]["subreddit"]
    data = get_latest_data_by_subreddit("analyzed_subscriptions", subreddit)

    if not data:
        return jsonify({"error": "No analyzed data found for this subreddit"}), 404
    
    return jsonify(data)