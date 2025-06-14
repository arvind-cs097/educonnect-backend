from datetime import datetime, timezone
from app.extensions import db

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    log_level = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    context = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    user = db.relationship('User', backref=db.backref('logs', lazy=True))

    def __repr__(self):
        return f'<Log {self.log_level} - {self.message[:50]}>'