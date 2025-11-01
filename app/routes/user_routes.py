from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app.services.db import get_db
from app.helpers.jwt_utils import is_token_revoked

bp = Blueprint("user", __name__)

@bp.route("/who_am_i", methods=["GET"])
@jwt_required()
def who_am_i():
    if is_token_revoked():
        return jsonify({"msg": "Token revoked"}), 401
    
    user_id = get_jwt_identity()
    db, client = get_db()

    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
       
        if not user:
            return jsonify({"msg": "User not found"}), 404

        return jsonify(
            id=str(user["_id"]),
            username=user["username"]
            # Add email if needed
        )
    
    finally:
        client.close()