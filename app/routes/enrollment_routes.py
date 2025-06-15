from flask import Blueprint, jsonify, request
from app.models import Enrollment, Course, User
from app.utils import login_required, token_not_blacklisted
from app.extensions import db

enrollment_bp = Blueprint('enrollment', __name__)

@enrollment_bp.route('/api/enroll', methods=['POST'])
@token_not_blacklisted
@login_required
def enroll_in_course(current_user):
    try:
        data = request.get_json()
        course_id = data.get('course_id')
        if not course_id:
            return jsonify({"status": "error", "message": "Course ID is required"}), 400

        course = db.session.get(Course, course_id)
        if not course:
            return jsonify({"status": "error", "message": "Course not found"}), 404

        existing_enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
        if existing_enrollment:
            return jsonify({"status": "error", "message": "Already enrolled in this course"}), 400

        new_enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
        db.session.add(new_enrollment)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"Enrolled in course '{course.title}' successfully"
        }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@enrollment_bp.route('/api/enrolled-courses', methods=['GET'])
@token_not_blacklisted
@login_required
def get_enrolled_courses(current_user):
    try:
        enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()

        course_list = [
            {
                "id": enrollment.course.id,
                "title": enrollment.course.title,
                "description": enrollment.course.description,
                "enrolled_at": enrollment.enrolled_at.isoformat()
            }
            for enrollment in enrollments
        ]

        return jsonify({"status": "success", "data": course_list}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@enrollment_bp.route('/api/enrollments/<int:course_id>', methods=['DELETE'])
@token_not_blacklisted
@login_required
def unenroll_from_course(current_user, course_id):
    try:
        course = db.session.get(Course, course_id)
        if not course:
            return jsonify({"status": "error", "message": "Course not found"}), 404

        enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
        if not enrollment:
            return jsonify({"status": "error", "message": "You are not enrolled in this course"}), 404

        db.session.delete(enrollment)
        db.session.commit()

        return jsonify({"status": "success", "message": "Successfully unenrolled from the course"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@enrollment_bp.route('/api/enrollments', methods=['GET'])
@token_not_blacklisted
@login_required
def get_all_enrollments(current_user):
    if current_user.role.name != 'admin':
        return jsonify({"status": "error", "message": "Unauthorized access"}), 403

    try:
        enrollments = Enrollment.query.all()
        enrollment_list = [
            {
                "enrollment_id": e.id,
                "user_id": e.user.id,
                "user_name": e.user.name,
                "course_id": e.course.id,
                "course_title": e.course.title,
                "enrolled_at": e.enrolled_at.isoformat()
            }
            for e in enrollments
        ]

        return jsonify({"status": "success", "data": enrollment_list}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@enrollment_bp.route('/api/my-course-enrollments', methods=['GET'])
@token_not_blacklisted
@login_required
def get_enrollments_for_my_courses(current_user):
    try:
        enrollments = Enrollment.query.join(Course).filter(Course.created_by == current_user.id).all()

        enrollment_list = [
            {
                "enrollment_id": e.id,
                "course_id": e.course.id,
                "course_title": e.course.title,
                "user_id": e.user.id,
                "user_name": e.user.name,
                "enrolled_at": e.enrolled_at.isoformat()
            }
            for e in enrollments
        ]

        return jsonify({"status": "success", "data": enrollment_list}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
