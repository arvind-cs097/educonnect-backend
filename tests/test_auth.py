import json
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash
from app.models import Role

def test_login_success_and_failure(client, setup_roles):
    if not db.session.get(Role, 3):
        db.session.add(Role(id=3, name="student"))
        db.session.commit()
        
    # Step 1: Create a test user in DB
    user = User(
        name='Test User',
        email='test@example.com',
        password=generate_password_hash('testpass'),
        role_id=3
    )
    db.session.add(user)
    db.session.commit()

    # Step 2: Successful login
    response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'testpass'
    })
    print("RESPONSE DATA:", response.get_data(as_text=True))
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data

    # Step 3: Failed login - wrong password
    response_fail = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'wrongpass'
    })
    assert response_fail.status_code == 401
    fail_data = response_fail.get_json()
    assert fail_data['status'] == 'error'
