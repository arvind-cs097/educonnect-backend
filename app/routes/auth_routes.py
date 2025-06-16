from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User
from app.utils import generate_token, login_required
from app.redis_client import redis_client
from app.extensions import db
import jwt, os
from datetime import datetime, timezone

auth_bp = Blueprint("auth", __name__)#, url_prefix="/api/auth"
SECRET_KEY = os.environ.get("SECRET_KEY")

@auth_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"status": "error", "message": "Missing email or password"}), 400

        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404

        # NEW (secure):
        if not check_password_hash(user.password, data['password']):
            # fallback for old users with plain text passwords
            if user.password != data['password']:
                return jsonify({"status": "error", "message": "Incorrect password"}), 401
            if user.password == data['password']:
                # User is using a plain-text password, so upgrade it
                user.password = generate_password_hash(data['password'])
                db.session.commit()

        print("Role", user.role.name)
        token = generate_token(user.id)

        return jsonify({
            "status": "success",
            "message": "Login successful",
            "token": token,
            "data": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role.name
            }
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@auth_bp.route('/api/logout', methods=["POST"])
@login_required
def logout(current_user):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token:
        # Decode token to get expiration time
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        exp_timestamp = decoded_token.get("exp")

        token_key = f"blacklist:{token}"

        if exp_timestamp:
            current_time = datetime.now(timezone.utc).timestamp()
            ttl = int(exp_timestamp - current_time)
            # Only set the key if the token hasn't expired already
            if ttl > 0:
                redis_client.setex(token_key, ttl, 'blacklisted')

        else:
            # Fallback: set a default expiry (e.g., 1 hour)
            redis_client.setex(token_key, 3600, 'blacklisted')

        return jsonify({"status": "success", "message": "Logged out successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "No token provided"}), 400
