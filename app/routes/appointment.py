from flask import Blueprint, request, jsonify, render_template, make_response
from app.extensions import db
from app.models.appointment import Appointment
from app.models.user import User
from app.models.waitlist import Waitlist
from datetime import datetime
import csv
import io

appointment_bp = Blueprint('appointment', __name__, url_prefix='/appointments')

@appointment_bp.route('', methods=['POST'])
def create_appointment():
    data = request.get_json()
    student_id = data.get('student_id')
    advisor_id = data.get('advisor_id')
    time_str = data.get('time')

    if not all([student_id, advisor_id, time_str]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        time = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid time format. Use YYYY-MM-DD HH:MM'}), 400

    student = User.query.get(student_id)
    advisor = User.query.get(advisor_id)
    if not student or not advisor:
        return jsonify({'error': 'Student or advisor not found'}), 404

    new_appointment = Appointment(
        student_id=student_id,
        advisor_id=advisor_id,
        time=time,
        status='scheduled'
    )

    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({
        'message': 'Appointment created',
        'appointment_id': new_appointment.id
    }), 201

@appointment_bp.route('', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    results = []

    for a in appointments:
        results.append({
            'id': a.id,
            'student_id': a.student_id,
            'advisor_id': a.advisor_id,
            'time': a.time.strftime('%Y-%m-%d %H:%M'),
            'status': a.status
        })

    return jsonify(results), 200

@appointment_bp.route('/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    # Try to find a matching waitlist entry
    match = Waitlist.query.filter_by(
        advisor_id=appointment.advisor_id,
        desired_time=appointment.time,
        status='waiting'
    ).order_by(Waitlist.created_at).first()

    if match:
        # Create a new appointment using waitlist student
        new_appt = Appointment(
            student_id=match.student_id,
            advisor_id=match.advisor_id,
            time=match.desired_time,
            status='scheduled'
        )
        db.session.add(new_appt)
        match.status = 'filled'

    db.session.delete(appointment)
    db.session.commit()

    return jsonify({'message': f'Appointment {appointment_id} cancelled'}), 200

@appointment_bp.route('/view', methods=['GET'])
def appointment_table():
    appointments = Appointment.query.all()

    data = []
    for a in appointments:
        data.append({
            'id': a.id,
            'student_name': User.query.get(a.student_id).name,
            'advisor_name': User.query.get(a.advisor_id).name,
            'time': a.time.strftime('%Y-%m-%d %H:%M'),
            'status': a.status
        })

    return render_template('appointments_page.html', appointments=data)

@appointment_bp.route('/export', methods=['GET'])
def export_appointments_csv():
    appointments = Appointment.query.all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Student', 'Advisor', 'Time', 'Status'])

    for a in appointments:
        writer.writerow([
            a.id,
            User.query.get(a.student_id).name,
            User.query.get(a.advisor_id).name,
            a.time.strftime('%Y-%m-%d %H:%M'),
            a.status
        ])

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=appointments.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response
