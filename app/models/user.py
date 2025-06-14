from datetime import datetime, timezone
from app.extensions import db

class User(db.Model):
    # Table name will be 'users' by default (same as class name in lowercase)
    __tablename__ = 'users'
    
    # Define the columns corresponding to the database table
    id = db.Column(db.Integer, primary_key=True)  # id column (Primary Key)
    name = db.Column(db.String(100), nullable=False)  # name column
    email = db.Column(db.String(150), unique=True, nullable=False)  # email column (unique)
    password = db.Column(db.String(255), nullable=False)  # password column (hashed)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)  # Foreign Key (role_id)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Define the relationship to the Role model (One to Many from Role to User)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f'<User {self.name}>'