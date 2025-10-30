from bson import ObjectId
from flask_jwt_extended import get_jwt_identity
from app.services.db import fetch_collection_data

def get_current_user_id():
    current_user = get_jwt_identity()

    try:
        current_user_id = ObjectId(current_user)
    except Exception as e:
        raise ValueError("Invalid user ID format: " + str(e))
    
    try:
        user_record = fetch_collection_data("users", {"_id": current_user_id})
        if not user_record:
            raise ValueError("User not found in database")
    except Exception as e:
        raise ValueError("Failed to validate user ID: " + str(e))

    return current_user_id