from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from app.services.db import connect_db
import datetime
from datetime import timedelta
import re
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from app.schema.user import user_schema

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
    username = request.json.get("username").lower()
    email = request.json.get("email").lower()
    password = request.json.get("password")
    hashed_password = generate_password_hash(password)
 
    new_user = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "last_login": None,
        "revoked_access_tokens": [],
        "refresh_revoked": False
    }

    """
    Jsonschema validate function below compares new user to the user schema to
    validate the correct data before database insertion.
    
    Type checking and validation messages are included to the schema and can be modified if needed
    Try using postman, user obj {"username":"name","email":"mail","password":"password"}
    User schema can be found here: app/schema/user.
    Read more about jsonschema: https://json-schema.org/learn
    """

    try:
        validate(instance=new_user, schema=user_schema)
    except ValidationError as e:
        return jsonify({"msg": e.schema["validationMessage"]}), 400

    
    client,db = connect_db()

    if db.users.find_one({"username": username}):
        return jsonify({"msg": "Username already exists"}), 400

    if db.users.find_one({"email": email}):
        return jsonify({"msg": "Email already registered"}), 400
    
    result = db.users.insert_one(new_user)

    return jsonify({"msg": "User created successfully",
                        "user_id": str(result.inserted_id) }), 




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
