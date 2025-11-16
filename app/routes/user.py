from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app.services.db import fetch_data_from_collection
from app.helpers.jwt_utils import is_token_revoked

user_bp = Blueprint("user", __name__)

@user_bp.route("/who_am_i", methods=["GET"])
@jwt_required()
def who_am_i():
    if is_token_revoked():
        return jsonify({"msg": "Token revoked"}), 401
    
    user_id = get_jwt_identity()
    
    users = fetch_data_from_collection("users", {"_id": ObjectId(user_id)})
    
    if not users:
        return jsonify({"msg": "User not found"}), 404
    
    user = users[0]

    return jsonify(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"],
        created_at=user.get("created_at") #returns None if not present
    )

