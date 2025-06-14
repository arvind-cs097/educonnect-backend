from datetime import datetime, timezone
from app.extensions import db

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # This line sets up the relationship from Course to User (the creator)
    created_by_user = db.relationship('User', backref=db.backref('courses', lazy=True))

    def __repr__(self):
        return f'<Course {self.title}>'