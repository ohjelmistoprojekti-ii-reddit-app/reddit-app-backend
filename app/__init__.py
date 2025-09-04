from flask import Flask
  
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    from app.routes.items import bp as items_bp
    app.register_blueprint(items_bp)

    return app
