from datetime import datetime, timezone
from app.extensions import db

class Announcement(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    created_by_user = db.relationship('User', backref=db.backref('announcements_created', lazy=True))
    course = db.relationship('Course', backref=db.backref('announcements', lazy=True))

    def __repr__(self):
        return f'<Announcement {self.title}>'