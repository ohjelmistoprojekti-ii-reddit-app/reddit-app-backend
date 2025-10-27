from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    db, client = get_db()
    user = db.users.find_one({"username": username})
    client.close()

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"msg": "Wrong username or password"}), 401

    access_token = create_access_token(identity=str(user["_id"]))
    refresh_token = create_refresh_token(identity=str(user["_id"]))

    return jsonify(access_token=access_token, refresh_token=refresh_token)


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)


@bp.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    
    db, client = get_db()
    existing_user = db.users.find_one({"username": username})
    if existing_user:
        client.close()
        return jsonify({"msg": "Username already exists"}), 400

    last_user = db.users.find_one(sort=[("id", -1)])
    if not last_user:
        next_user_id = 1 
    else:
        next_user_id = last_user["id"] + 1
 
    hashed_password = generate_password_hash(password)
    
    new_user = {
        "id": next_user_id,
        "username": username,
        "email": email,
        "password": hashed_password
    }

    result = db.users.insert_one(new_user)
    client.close()

    return jsonify({"msg": "User created successfully", "user_id": str(result.inserted_id)}), 201



