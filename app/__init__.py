from flask import Flask
from flask_cors import CORS
from app.routes.routes import bp
from app.routes.authentication_routes import bp as authentication_bp
from app.routes.countries import countries_bp
# from app.routes.reddit_api import reddit_api_bp
# from app.routes.statistics import statistics_bp
from app.routes.subbreddits import subbreddits_bp
# from app.routes.topics import topics_bp
from app.routes.user_routes import bp as user_bp
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
    
    CORS(
        app,
        origins=allowed_origins,
        supports_credentials=True,
        methods=["GET", "POST", "DELETE", "OPTIONS", "PATCH"], 
        allow_headers=["Content-Type", "Authorization"],
        )

    jwt = JWTManager(app)

    app.register_blueprint(bp)
    app.register_blueprint(authentication_bp)
    app.register_blueprint(countries_bp)
    # app.register_blueprint(reddit_api_bp)
    # app.register_blueprint(statistics_bp)
    app.register_blueprint(subbreddits_bp)
    # app.register_blueprint(topics_bp)
    app.register_blueprint(user_bp)
    
    return app
