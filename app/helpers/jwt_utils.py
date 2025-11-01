from flask_jwt_extended import get_jwt, get_jwt_identity
import datetime
from bson import ObjectId
from app.services.db import get_db

def is_token_revoked():
    jwt_data = get_jwt()
    jti = jwt_data["jti"]
    user_id = get_jwt_identity()
    
    db, client = get_db()
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return True

        now = datetime.datetime.now(datetime.timezone.utc)
        for revoked in user.get("revoked_access_tokens", []):
            if revoked["jti"] == jti and revoked["exp"] > now:
                return True
        return False
    
    finally:
        client.close()