from flask import Flask
from flask_cors import CORS
from app.routes.routes import bp as posts_bp
from app.routes.subreddit_routes import bp as subreddit_bp
from app.routes.countries_routes import bp as countries_bp
from app.routes.subscriptions_routes import bp as subscriptions_bp
from app.routes.authentication_routes import bp as authentication_bp
from app.routes.user_routes import bp as user_bp
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    app.config.from_object('app.config.Config')
    app.register_blueprint(posts_bp)
    app.register_blueprint(subreddit_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(subscriptions_bp)
    app.register_blueprint(authentication_bp)
    app.register_blueprint(user_bp)

    print(app.url_map)
    
    return app
