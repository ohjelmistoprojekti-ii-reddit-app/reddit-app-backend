from flask import Flask
from flask_cors import CORS
from app.routes.routes import bp as posts_bp
from app.routes.subreddit_routes import bp as subreddit_bp
from app.routes.countries_routes import bp as countries_bp
from app.routes.test_routes import bp as test_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.config.Config')
    app.register_blueprint(posts_bp)
    app.register_blueprint(subreddit_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(test_bp)
    
    return app
