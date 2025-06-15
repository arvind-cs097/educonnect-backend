from flask import Flask
from app.extensions import db
from flask_migrate import Migrate
from config import config
from .routes import all_blueprints

# db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=None):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class or config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register routes (later)
    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app
