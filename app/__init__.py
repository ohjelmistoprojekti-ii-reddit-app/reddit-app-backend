from flask import Flask
from flask_cors import CORS
from app.routes.authentication import authentication_bp
from app.routes.countries import countries_bp
from app.routes.posts import posts_bp
from app.routes.statistics import statistics_bp
from app.routes.subbreddits import subbreddits_bp
from app.routes.subscriptions import subscriptions_bp
from app.routes.topics import topics_bp
from app.routes.user import user_bp
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

    app.register_blueprint(authentication_bp, url_prefix='api/authentication')
    app.register_blueprint(countries_bp, url_prefix='api/countries')
    app.register_blueprint(posts_bp, url_prefix='api/posts')
    app.register_blueprint(statistics_bp, url_prefix='api/statistics')
    app.register_blueprint(subbreddits_bp, url_prefix='api/subreddits')
    app.register_blueprint(subscriptions_bp, url_prefix='api/subscriptions')
    app.register_blueprint(topics_bp, url_prefix='api/topics')
    app.register_blueprint(user_bp, url_prefix='api/user')
    
    
    return app
