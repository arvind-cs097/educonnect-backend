from datetime import datetime, timezone
from app.extensions import db

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.Text, nullable=False)
    file_size = db.Column(db.BigInteger, nullable=True)
    file_type = db.Column(db.String(50), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('files', lazy=True))

    def __repr__(self):
        return f'<File {self.file_name}>'