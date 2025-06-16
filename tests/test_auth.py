import json
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash

def test_login_success_and_failure(client, setup_roles, student_user):
    # Step 1: Successful login
    response = client.post('/api/login', json={
        'email': 'student@example.com',
        'password': 'studentpass'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data

    # Step 2: Failed login - wrong password
    response_fail = client.post('/api/login', json={
        'email': 'student@example.com',
        'password': 'wrongpass'
    })
    assert response_fail.status_code == 401
    fail_data = response_fail.get_json()
    assert fail_data['status'] == 'error'
