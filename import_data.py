import pandas as pd
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.appointment import Appointment
from datetime import datetime

app = create_app()
app.app_context().push()

df = pd.read_excel("/Users/dc/Desktop/Career Services Appointments Report 180 Days.xlsx")

def get_or_create_user(name, role):
    user = User.query.filter_by(name=name, role=role).first()
    if not user:
        email = name.lower().replace(" ", ".") + "@example.com"
        user = User(name=name, email=email, role=role)
        db.session.add(user)
        db.session.commit()
    return user

created_count = 0

status_map = {
    'completed': 'completed',
    'cancelled': 'cancelled',
    'canceled': 'cancelled',
    'noshow': 'no-show',
    'no-show': 'no-show',
    'no show': 'no-show',
    'scheduled': 'scheduled'
}

for idx, row in df.iterrows():
    try:
        student_name = str(row['Student College (at Appt. Time) Name']).strip()
        advisor_name = f"{row['Staff Member First Name']} {row['Staff Member Last Name']}".strip()
        time = pd.to_datetime(row['Appointments Start Date Date'])

        raw = str(row['Appointments Status']).strip().lower().replace("_", "").replace(" ", "")
        status = status_map.get(raw, 'scheduled')

        student = get_or_create_user(student_name, "student")
        advisor = get_or_create_user(advisor_name, "advisor")

        exists = Appointment.query.filter_by(
            student_id=student.id,
            advisor_id=advisor.id,
            time=time
        ).first()

        if not exists:
            appt = Appointment(
                student_id=student.id,
                advisor_id=advisor.id,
                time=time,
                status=status
            )
            db.session.add(appt)
            created_count += 1
    except Exception as e:
        print(f"Skipped row {idx}: {e}")

db.session.commit()
print(f"Imported {created_count} appointments.")
