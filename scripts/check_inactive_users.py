from app.services.db import fetch_collection_data, update_collection_data
from datetime import datetime, timezone, timedelta
import sys

def check_inactive_users_and_subscriptions():
    current_date = datetime.now(timezone.utc)
    max_date = current_date - timedelta(days=15)

    errors = []
    try:
        # Fetch users who have not logged in for more than 15 days
        inactive_users = fetch_collection_data("users", {"last_login": {"$lt": max_date}})
        if not inactive_users:
            return {
                "inactive_users_found": 0,
                "no_active_subscriptions": 0,
                "subscriptions_deactivated": 0,
                "errors": []
            }
    except Exception as e:
        errors.append(f"Error while fetching users: {e}")

    inactive_users_found = 0
    no_active_subscriptions = 0
    subscriptions_deactivated = 0

    for user in inactive_users:
        user_id = user['_id']
        inactive_users_found += 1
        try:
            user_subscription = fetch_collection_data("subscriptions", {"subscribers": user_id})
        except Exception as e:
            errors.append(f"Error while fetching subscriptions for user '{user_id}': {e}")
            continue
        
        if not user_subscription:
            no_active_subscriptions += 1
            continue

        subreddit = user_subscription[0]["subreddit"]
        analysis_type = user_subscription[0]["analysis_type"]

        try:
            # Remove inactive user from subscribers list
            update_collection_data(
                "subscriptions",
                {"subreddit": subreddit, "analysis_type": analysis_type, "active": True},
                {"$pull": {"subscribers": user_id}}
            )

            subscriptions_deactivated += 1
        except Exception as e:
            errors.append(f"Error while removing user '{user_id}' from subscription to '{subreddit}': {e}")
            continue

        try:
            set_to_inactive = False
            # Check if subscribers list is empty, and set subscription to inactive if it is
            updated_subscription = fetch_collection_data(
                "subscriptions",
                {"subreddit": subreddit, "analysis_type": analysis_type, "active": True}
            )

            if updated_subscription and len(updated_subscription[0]["subscribers"]) == 0:
                update_collection_data(
                    "subscriptions",
                    {"subreddit": subreddit, "analysis_type": analysis_type, "active": True},
                    {"$set": {"active": False}}
                )
                set_to_inactive = True
        except Exception as e:
            errors.append(f"Error while checking subscription status for subreddit '{subreddit}': {e}")
            continue

        if set_to_inactive:
            print(f"User '{user_id}' removed from subscription to subreddit '{subreddit}'.\nNo active subscribers remain, so '{subreddit}' is set to inactive.")
        else:
            print(f"User '{user_id}' removed from subscription to subreddit '{subreddit}'.")

    results = {
        "inactive_users_found": inactive_users_found,
        "no_active_subscriptions": no_active_subscriptions,
        "subscriptions_deactivated": subscriptions_deactivated,
        "errors": errors
    }

    return results

if __name__ == "__main__":
    results = check_inactive_users_and_subscriptions()

    if results:
        print("==== CHECK COMPLETE ====")
        print(f"Inactive users found: {results['inactive_users_found']}")
        print(f"Inactive users with no active subscriptions: {results['no_active_subscriptions']}")
        print(f"Subscriptions deactivated: {results['subscriptions_deactivated']}")

        if results['errors']:
            print("Errors occurred during the process:")
            for error in results['errors']:
                print(f"- {error}")

            # Make sure that GitHub Actions workflow fails if any errors occurred
            sys.exit(1)