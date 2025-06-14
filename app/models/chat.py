from datetime import datetime, timezone
from app.extensions import db

class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    message = db.Column(db.LargeBinary, nullable=False)
    file_url = db.Column(db.Text, nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref=db.backref('sent_chats', lazy=True))
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref=db.backref('received_chats', lazy=True))
    course = db.relationship('Course', backref=db.backref('chats', lazy=True))

    def __repr__(self):
        return f'<Chat from {self.sender_id} to {self.receiver_id}>'