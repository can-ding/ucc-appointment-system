from app.extensions import db

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    advisor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False) 
    def __repr__(self):
        return f"<Appointment {self.id} {self.status}>"
