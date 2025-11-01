from flask import Flask
from flask_cors import CORS
from app.routes.statistics import statistics_bp
from app.routes.topics import topics_bp
from app.routes.reddit_api import reddit_api_bp
from app.routes.subbreddits import subbreddits_bp
from app.routes.countries import countries_bp
# Old api file ready to be removed
from app.routes.routes import bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.config.Config')
    # Old api blueprint ready to be removed
    app.register_blueprint(bp)
    
    app.register_blueprint(subbreddits_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(topics_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(reddit_api_bp)
    
    return app
