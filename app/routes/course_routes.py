from flask import Blueprint, request, jsonify
from app.models import Course, Enrollment
from app.extensions import db
from app.utils import login_required, token_not_blacklisted

course_bp = Blueprint('course', __name__)

@course_bp.route('/api/courses', methods=['GET'])
def get_courses():
    try:
        courses = Course.query.all()
        course_list = [
            {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "created_at": course.created_at.isoformat(),
                "updated_at": course.updated_at.isoformat(),
                "created_by": course.created_by_user.name
            }
            for course in courses
        ]
        return jsonify({"status": "success", "data": course_list}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@course_bp.route('/api/courses', methods=['POST'])
@token_not_blacklisted
@login_required
def create_course(current_user):
    try:
        data = request.get_json()

        if current_user.role.name.lower() not in ['admin', 'teacher']:
            return jsonify({"status": "error", "message": "You are not authorized to create a course"}), 403

        if not data.get("title") or not data.get("description"):
            return jsonify({"status": "error", "message": "Missing title or description"}), 400

        existing_course = Course.query.filter_by(title=data["title"]).first()
        if existing_course:
            return jsonify({"status": "error", "message": "Course with this title already exists"}), 400

        new_course = Course(
            title=data["title"],
            description=data["description"],
            created_by=current_user.id
        )

        db.session.add(new_course)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Course created successfully",
            "data": {"id": new_course.id, "title": new_course.title}
        }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@course_bp.route('/api/my-courses', methods=['GET'])
@token_not_blacklisted
@login_required
def get_my_courses(current_user):
    try:
        courses = Course.query.filter_by(created_by=current_user.id).all()
        course_list = [
            {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "created_at": course.created_at.isoformat(),
                "updated_at": course.updated_at.isoformat()
            }
            for course in courses
        ]
        return jsonify({"status": "success", "data": course_list}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@course_bp.route('/api/courses/<int:course_id>', methods=['PUT'])
@token_not_blacklisted
@login_required
def update_course(current_user, course_id):
    try:
        course = Course.query.get(course_id)
        if not course:
            return jsonify({"status": "error", "message": "Course not found"}), 404

        if current_user.id != course.created_by and current_user.role.name.lower() != 'admin':
            return jsonify({"status": "error", "message": "Not authorized to update this course"}), 403

        data = request.get_json()
        title = data.get("title")
        description = data.get("description")

        if title:
            course.title = title
        if description:
            course.description = description

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Course updated successfully",
            "data": {
                "id": course.id,
                "title": course.title,
                "description": course.description
            }
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@course_bp.route('/api/courses/<int:course_id>', methods=['DELETE'])
@token_not_blacklisted
@login_required
def delete_course(current_user, course_id):
    try:
        course = Course.query.get(course_id)
        if not course:
            return jsonify({"status": "error", "message": "Course not found"}), 404

        if current_user.id != course.created_by and current_user.role.name.lower() != 'admin':
            return jsonify({"status": "error", "message": "Not authorized to delete this course"}), 403

        db.session.delete(course)
        db.session.commit()

        return jsonify({"status": "success", "message": "Course deleted successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
