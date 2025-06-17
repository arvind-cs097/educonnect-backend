from flask import Flask
from app.extensions import db
from flask_migrate import Migrate
from config import config
from .routes import all_blueprints
# from app.models import Role

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

    # Create tables and seed roles (safe to run every time)
    # with app.app_context():
    #     db.create_all()
    #     seed_roles()

    return app

# def seed_roles():
#     default_roles = ['admin', 'teacher', 'student']

#     for role_name in default_roles:
#         existing = Role.query.filter_by(name=role_name).first()
#         if not existing:
#             db.session.add(Role(name=role_name))

#     db.session.commit()
