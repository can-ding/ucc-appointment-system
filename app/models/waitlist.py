from app.extensions import db
from datetime import datetime

class Waitlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    advisor_id = db.Column(db.Integer, nullable=False)
    desired_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='waiting')  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
