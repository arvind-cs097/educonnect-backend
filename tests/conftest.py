import pytest
from app import create_app
from app.extensions import db
from config import TestConfig
from app.models import Role
from app.models import Course
from app.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = create_app(TestConfig)
    app.testing = True
    app.debug = True

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def setup_roles():
    """Fixture to populate the roles table with default roles."""
    roles = [
        Role(id=1, name='Admin'),
        Role(id=2, name='Instructor'),
        Role(id=3, name='Student'),
    ]
    db.session.add_all(roles)
    db.session.commit()

@pytest.fixture
def teacher_user(setup_roles):
    user = User(
        name="Test User",
        email="testuser@example.com",
        password=generate_password_hash("testpass"),
        role_id=2
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def teacher_auth_headers(client, teacher_user):
    response = client.post("/api/login", json={
        "email": "testuser@example.com",
        "password": "testpass"
    })
    token = response.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def student_user(setup_roles):
    user = User(
        name="Student User",
        email="student@example.com",
        password=generate_password_hash("studentpass"),
        role_id=3  # Student
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def student_auth_headers(client, student_user):
    response = client.post("/api/login", json={
        "email": "student@example.com",
        "password": "studentpass"
    })
    token = response.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_courses(teacher_user):
    course1 = Course(title="Math 101", description="Basic Math", created_by=teacher_user.id)
    course2 = Course(title="Science 101", description="Intro to Science", created_by=teacher_user.id)
    course3 = Course(title="Flask Bootcamp", description="Learn Flask", created_by=teacher_user.id)
    db.session.add_all([course1, course2, course3])
    db.session.commit()
