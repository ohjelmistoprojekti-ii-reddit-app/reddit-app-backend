from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from app.services.db import connect_db
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

    client, db = connect_db()
    try:
        user = db.users.find_one({"username": username})
        
        if not user or not check_password_hash(user["password"], password):
            return jsonify({"msg": "Wrong username or password"}), 401
        
        db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "last_login": datetime.datetime.now(datetime.timezone.utc),
                "refresh_revoked": False
            }}
        )

        access_token = create_access_token(identity=str(user["_id"]))
        refresh_token = create_refresh_token(identity=str(user["_id"]))

        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    
    finally:
        client.close()


@authentication_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    client, db = connect_db()
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user or user.get("refresh_revoked"):
            return jsonify({"msg": "Refresh token revoked"}), 401

        new_access_token = create_access_token(identity=user_id)
        return jsonify(access_token=new_access_token), 200
    
    finally:
        client.close()


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
    
    client, db = connect_db()
    try:
        if db.users.find_one({"username": username.lower()}):
            return jsonify({"msg": "Username already exists"}), 400

        if db.users.find_one({"email": email.lower()}):
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

        result = db.users.insert_one(new_user)

        return jsonify({
            "msg": "User created successfully",
            "user_id": str(result.inserted_id)
        }), 201

    finally:
        client.close()


@authentication_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    jti = get_jwt()["jti"]
    exp_timestamp = datetime.datetime.fromtimestamp(get_jwt()["exp"], datetime.timezone.utc)
    now = datetime.datetime.now(datetime.timezone.utc)

    client, db = connect_db()
    try:
        fifteen_minutes_ago = now - timedelta(minutes=15)

        # Delete revoked access tokens older than 15 minutes
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"revoked_access_tokens": {"exp": {"$lt": fifteen_minutes_ago}}}}
        )

        # Add a newly revoked access token to the database
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"revoked_access_tokens": {"jti": jti, "exp": exp_timestamp}}}
        )

        # Revoke refresh token
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"refresh_revoked": True}}
        )

        return jsonify(msg="Access and refresh token revoked"), 200
    
    finally:
        client.close()

@authentication_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    if is_token_revoked():
        return jsonify({"msg": "Token revoked"}), 401
        
    user_id = get_jwt_identity()
    client, db = connect_db()
    try:
        subscription = db.subscriptions.find_one({"subscribers": ObjectId(user_id), "active": True})
        if subscription:
            # Remove user from subscribers list
            db.subscriptions.update_one(
                {"_id": subscription["_id"]},
                {"$pull": {"subscribers": ObjectId(user_id)}}
            )

        updated_sub = db.subscriptions.find_one({"_id": subscription["_id"]})
        if len(updated_sub["subscribers"]) == 0:
            db.subscriptions.update_one(
                {"_id": subscription["_id"]},
                {"$set": {"active": False}}
            )

        user_deletion_result = db.users.delete_one({"_id": ObjectId(user_id)})
        
        if user_deletion_result.deleted_count == 0:
            return jsonify({"msg": "User not found"}), 404

        return jsonify({"msg": "User deleted successfully"}), 200
    
    finally:
        client.close()
    
