from flask import Flask
from flask_cors import CORS
from app.services.db_init import populate_database_reddit_posts

  
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.config.Config')
    # populates the database with reddit post when running the app
    populate_database_reddit_posts()
    from app.routes.routes import bp as posts_bp
    app.register_blueprint(posts_bp)

    
    return app
