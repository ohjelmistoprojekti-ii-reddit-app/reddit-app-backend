from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app.services.db import get_db

bp = Blueprint("user", __name__)

@bp.route("/who_am_i", methods=["GET"])
@jwt_required()
def who_am_i():
    db, client = get_db()
    user_id = get_jwt_identity()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    client.close()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify(
        id=str(user["_id"]),
        username=user["username"],
        # Add email if needed
    )