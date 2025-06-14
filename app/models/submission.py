from datetime import datetime, timezone
from app.extensions import db

class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    grade = db.Column(db.String(20))
    feedback = db.Column(db.String(250))
    file_url = db.Column(db.Text, nullable=False)

    # Relationships for accessing the assignment and user from the submission
    assignment = db.relationship('Assignment', backref=db.backref('submissions', lazy=True))
    user = db.relationship('User', backref=db.backref('submissions', lazy=True))

    def __repr__(self):
        return f'<Submission User {self.user_id} for Assignment {self.assignment_id}>'