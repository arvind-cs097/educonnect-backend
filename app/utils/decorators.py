from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.models import User
from app.redis_client import redis_client
from app.extensions import db

def verify_token():
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return jsonify({"status": "error", "message": "Token is missing!"}), 401

    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        user = db.session.get(User, payload["user_id"])
        if not user:
            return jsonify({"status": "error", "message": "User not found!"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"status": "error", "message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"status": "error", "message": "Invalid token!"}), 401

    return user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = verify_token()
        if not isinstance(result, User):
            return result
        return f(current_user=result, *args, **kwargs)
    return decorated_function

def token_not_blacklisted(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"status": "error", "message": "Token is missing!"}), 401

        # Check if token is blacklisted
        if redis_client.get(f"blacklist:{token}"):
            return jsonify({"status": "error", "message": "Token has been logged out"}), 401

        return f(*args, **kwargs)
    return decorated
