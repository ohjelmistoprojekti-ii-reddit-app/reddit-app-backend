from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from app.services.db import fetch_data_from_collection, update_one_item_in_collection, save_data_to_database, delete_one_item_from_collection
from app.helpers.jwt_utils import is_token_revoked
import datetime
from datetime import timedelta
import re

authentication_bp = Blueprint('authentication', __name__)

@authentication_bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    
    users = fetch_data_from_collection("users", {"username": username})
    if not users:
        return jsonify({"msg": "Wrong username or password"}), 401

    user = users[0]

    if not check_password_hash(user["password"], password):
        return jsonify({"msg": "Wrong username or password"}), 401

    update_one_item_in_collection(
        "users",
        {"_id": ObjectId(user["_id"])},
        {"$set": {
            "last_login": datetime.datetime.now(datetime.timezone.utc),
            "refresh_revoked": False
        }}
    )

    access_token = create_access_token(identity=user["_id"])
    refresh_token = create_refresh_token(identity=user["_id"])

    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@authentication_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    users = fetch_data_from_collection("users", {"_id": ObjectId(user_id)})
    
    if not users:
        return jsonify({"msg": "Refresh token revoked"}), 401 
    
    user = users[0]
    if user.get("refresh_revoked"):
        return jsonify({"msg": "Refresh token revoked"}), 401 
        
    new_access_token = create_access_token(identity=user_id)
    return jsonify(access_token=new_access_token), 200
    


@authentication_bp.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    if not username or not email or not password:
        return jsonify({"msg": "All fields (username, email, password) required"}), 400
    
    if len(password) < 8:
        return jsonify({"msg": "Password must be at least 8 characters"}), 400

    if len(username) < 3 or len(username) > 20:
        return jsonify({"msg": "Username must be from 3 to 20 characters"}), 400
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"msg": "Invalid email format"}), 400
    
    if fetch_data_from_collection("users", {"username": username.lower()}):
        return jsonify({"msg": "Username already exists"}), 400

    if fetch_data_from_collection("users", {"email": email.lower()}):
        return jsonify({"msg": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)
    new_user = {
        "username": username.lower(),
        "email": email.lower(),
        "password": hashed_password,
        "last_login": None,
        "revoked_access_tokens": [],
        "refresh_revoked": False,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    save_data_to_database(new_user, "users")

    return jsonify({
        "msg": "User created successfully",
        "user_id": str(new_user["_id"])
    }), 201



@authentication_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    token_data = get_jwt()

    jti = token_data["jti"]
    exp_timestamp = datetime.datetime.fromtimestamp(get_jwt()["exp"], datetime.timezone.utc)
    now = datetime.datetime.now(datetime.timezone.utc)
    fifteen_minutes_ago = now - timedelta(minutes=15)

    # Delete revoked access tokens older than 15 minutes
    update_one_item_in_collection(
        "users",
        {"_id": ObjectId(user_id)},
        {"$pull": {"revoked_access_tokens": {"exp": {"$lt": fifteen_minutes_ago}}}}
    )

    # Add a newly revoked access token to the database
    update_one_item_in_collection(
        "users",
        {"_id": ObjectId(user_id)},
        {"$push": {"revoked_access_tokens": {"jti": jti, "exp": exp_timestamp}}}
    )

    # Revoke refresh token
    update_one_item_in_collection(
        "users",
        {"_id": ObjectId(user_id)},
        {"$set": {"refresh_revoked": True}}
    )

    return jsonify(msg="Access and refresh token revoked"), 200
    

@authentication_bp.route("/delete_account", methods=["DELETE"])
@jwt_required()
def delete_user():

    if is_token_revoked():
        return jsonify({"msg": "Token revoked"}), 401
        
    user_id = ObjectId(get_jwt_identity())
    
    subscriptions = fetch_data_from_collection(
        "subscriptions", 
        {"subscribers": user_id, "active": True}
    )
    
    if subscriptions:
        subscription = subscriptions[0]
        # Remove user from subscribers list
        update_one_item_in_collection(
            "subscriptions",
            {"_id": ObjectId(subscription["_id"])},
            {"$pull": {"subscribers": user_id}}
        )

        updated_sub = fetch_data_from_collection(
            "subscriptions", 
            {"_id": ObjectId(subscription["_id"])}
        )[0]

        # Check if updated subscribers list is empty, and set subscription to inactive if it is
        if len(updated_sub["subscribers"]) == 0:
            update_one_item_in_collection(
                "subscriptions",
                {"_id": ObjectId(subscription["_id"])},
                {"$set": {"active": False}}
            )

    deletion_result = delete_one_item_from_collection(
        "users",
        {"_id": user_id}
    )

    if deletion_result == 0:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({"msg": "User deleted successfully"}), 200
