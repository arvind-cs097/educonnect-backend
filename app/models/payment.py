from datetime import datetime, timezone
from app.extensions import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), default='pending')
    payment_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)

    user = db.relationship('User', backref=db.backref('payments', lazy=True))
    course = db.relationship('Course', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f'<Payment {self.amount} for {self.payment_method} from User {self.user_id}>'