from flask_jwt_extended import get_jwt, get_jwt_identity
import datetime
from bson import ObjectId
from app.services.db import fetch_data_from_collection

def is_token_revoked():
    jwt_data = get_jwt()
    jti = jwt_data["jti"]
    user_id = get_jwt_identity()

    users = fetch_data_from_collection("users", {"_id": ObjectId(user_id)})
    if not users:
        return True
    
    user = users[0]

    now = datetime.datetime.now(datetime.timezone.utc)
    for revoked in user.get("revoked_access_tokens", []):
        if revoked["jti"] == jti and revoked["exp"] > now:
            return True
    return False