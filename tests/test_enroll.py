def test_enroll_course(client, student_auth_headers, sample_courses):
    enroll_response = client.post("/api/enroll", json={"course_id": 3}, headers=student_auth_headers)
    assert enroll_response.status_code == 201

    data = enroll_response.get_json()
    assert data["status"] == "success"
    assert "Enrolled" in data["message"]

    # Unenroll
    unenroll_response = client.delete(
        f"/api/enrollments/{3}",
        headers=student_auth_headers
    )
    assert unenroll_response.status_code == 200
    unenroll_data = unenroll_response.get_json()
    assert unenroll_data["status"] == "success"
    assert "unenrolled" in unenroll_data["message"]

    # Verify unenrollment from DB
    from app.models import Enrollment, User
    user = User.query.filter_by(email="student@example.com").first()
    enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=3).first()
    assert enrollment is None
