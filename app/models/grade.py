from datetime import datetime, timezone
from app.extensions import db

class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    graded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    feedback = db.Column(db.String(250))
    graded_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationship to access the Submission and the User who graded
    submission = db.relationship('Submission', backref=db.backref('grades', lazy=True))
    graded_by_user = db.relationship('User', backref=db.backref('graded_assignments', lazy=True))

    def __repr__(self):
        return f'<Grade for Submission {self.submission_id} graded by {self.graded_by}>'