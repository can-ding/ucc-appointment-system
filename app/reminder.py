from app import create_app
from app.extensions import db
from app.models.appointment import Appointment, User
from datetime import datetime, timedelta

app = create_app()
app.app_context().push()

now = datetime.now()
tomorrow = now + timedelta(days=1)

upcoming = Appointment.query.filter(
    Appointment.time >= now,
    Appointment.time <= tomorrow,
    Appointment.status.in_(["scheduled", "completed"])
).all()

if not upcoming:
    print("No upcoming appointments in the next 24 hours.")
else:
    print("Upcoming appointments in the next 24 hours:")
    for appt in upcoming:
        student = User.query.get(appt.student_id)
        advisor = User.query.get(appt.advisor_id)
        print(f" {appt.time.strftime('%Y-%m-%d %H:%M')} - Student: {student.name}, Advisor: {advisor.name}, Status: {appt.status}")
