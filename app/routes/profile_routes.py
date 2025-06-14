from flask import Blueprint, request, jsonify
from app.models import User
from app.utils import login_required, token_not_blacklisted
from app.extensions import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile', methods=['GET'])
@token_not_blacklisted
@login_required
def get_profile(current_user):
    try:
        profile_data = {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role.name,
            "created_at": current_user.created_at.isoformat(),
            "updated_at": current_user.updated_at.isoformat()
        }

        return jsonify({"status": "success", "data": profile_data}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@profile_bp.route('/api/profile', methods=['PUT'])
@token_not_blacklisted
@login_required
def update_profile(current_user):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        if not name and not email:
            return jsonify({"status": "error", "message": "No data provided to update"}), 400

        if email and email != current_user.email:
            # Check if the new email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({"status": "error", "message": "Email already in use"}), 400
            current_user.email = email

        if name:
            current_user.name = name

        db.session.commit()

        return jsonify({"status": "success", "message": "Profile updated successfully"}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
