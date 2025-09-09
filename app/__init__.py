from flask import Flask
from flask_cors import CORS

  
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.config.Config')

    from app.routes.routes import bp as posts_bp
    app.register_blueprint(posts_bp)

    

    



    return app
