from flask import Flask
from flask_cors import CORS
from app.routes.routes import bp as posts_bp
from app.routes.subreddit_routes import bp as subreddit_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.config.Config')
    app.register_blueprint(posts_bp)
    app.register_blueprint(subreddit_bp)
    
    return app
