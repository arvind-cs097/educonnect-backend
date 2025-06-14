from datetime import datetime, timezone
from app.extensions import db

class ScheduledJob(db.Model):
    __tablename__ = 'scheduled_jobs'

    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')
    scheduled_time = db.Column(db.DateTime, nullable=False)
    executed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<ScheduledJob {self.job_name} (Status: {self.status})>'