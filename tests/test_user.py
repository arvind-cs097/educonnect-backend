from app.models import User
from werkzeug.security import generate_password_hash
from app.extensions import db

def test_get_users(client, setup_roles):
    # Step 1: Add a user
    user = User(
        name="Sample User",
        email="sample@example.com",
        password=generate_password_hash("password123"),
        role_id=3  # Assuming Student
    )
    db.session.add(user)
    db.session.commit()

    # Step 2: Hit the API
    response = client.get("/api/users")

    # Step 3: Check response
    assert response.status_code == 200
    data = response.get_json()

    assert "data" in data
    assert isinstance(data["data"], list)
    assert any(u["email"] == "sample@example.com" for u in data["data"])

def test_create_user_success(client, setup_roles):
    # Define payload
    payload = {
        "name": "New User",
        "email": "newuser@example.com",
        "password": "securepassword",
        "role_id": 2
    }

    # Make POST request
    response = client.post("/api/users", json=payload)
    assert response.status_code == 201

    data = response.get_json()
    assert data["status"] == "success"
    assert data["message"] == "User created successfully"
    assert "id" in data["data"]

    # Check if user exists in DB
    user = User.query.filter_by(email=payload["email"]).first()
    assert user is not None
    