from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.appointment import Appointment
from app.models.user import User
from datetime import datetime

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

    db.session.delete(appointment)
    db.session.commit()

    return jsonify({'message': f'Appointment {appointment_id} cancelled'}), 200

