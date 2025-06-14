from flask import Blueprint, jsonify, request
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()

        user_list = [
            {"id": user.id, "name": user.name, "email": user.email, "role": user.role.name}
            for user in users
        ]

        return jsonify({"status": "success", "data": user_list}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@user_bp.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({"status": "error", "message": "User already exists with this email"}), 400

        hashed_password = generate_password_hash(data['password'])

        new_user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password,
            role_id=data.get('role_id')
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": "success", "message": "User created successfully", "data": {"id": new_user.id}}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
