from .auth_routes import auth_bp
from .user_routes import user_bp
from .course_routes import course_bp
from .enrollment_routes import enrollment_bp
from .profile_routes import profile_bp
from .main_routes import main_bp

all_blueprints = [auth_bp, user_bp, course_bp, enrollment_bp, profile_bp, main_bp]