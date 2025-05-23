from flask import Blueprint, jsonify
from app.models.appointment import Appointment
from app.models.user import User
from app.extensions import db
from sqlalchemy import func
from collections import defaultdict
from flask import jsonify
from sqlalchemy import func
from app.models.appointment import Appointment
from datetime import datetime
from flask import Blueprint, render_template, jsonify
from sqlalchemy import func
from app.models.appointment import Appointment
from app.models.waitlist import Waitlist

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/stats/summary', methods=['GET'])
def get_stats_summary():
    total = Appointment.query.count()
    completed = Appointment.query.filter_by(status='completed').count()
    cancelled = Appointment.query.filter_by(status='cancelled').count()
    no_show = Appointment.query.filter_by(status='no-show').count()

    top_advisors = db.session.query(
        User.name,
        func.count(Appointment.id).label("count")
    ).join(Appointment, Appointment.advisor_id == User.id)\
     .group_by(User.id)\
     .order_by(func.count(Appointment.id).desc())\
     .limit(3).all()

    top_advisors_list = [{"name": a[0], "count": a[1]} for a in top_advisors]

    return jsonify({
        "total_appointments": total,
        "completed_appointments": completed,
        "cancelled_appointments": cancelled,
        "no_show_appointments": no_show,
        "top_advisors": top_advisors_list
    })
@stats_bp.route('/stats/monthly', methods=['GET'])
def get_monthly_summary():
    results = db.session.query(
        func.strftime('%Y-%m', Appointment.time).label('month'),
        func.count(Appointment.id)
    ).group_by('month').order_by('month').all()

    monthly_data = [{"month": month, "count": count} for month, count in results]

    return jsonify({"appointments_per_month": monthly_data})

@stats_bp.route('/dashboard/monthly')
def render_monthly_chart():
    results = db.session.query(
        func.strftime('%Y-%m', Appointment.time).label('month'),
        func.count(Appointment.id)
    ).group_by('month').order_by('month').all()

    months = [r[0] for r in results]
    counts = [r[1] for r in results]

    return render_template('monthly_stats.html', months=months, counts=counts)
@stats_bp.route('/dashboard')
def dashboard():

    from datetime import datetime
    now = datetime.now()
    current_month = now.strftime('%Y-%m')
  
    recent_appointments_raw = db.session.query(Appointment).order_by(Appointment.time.desc()).limit(10).all()
    recent_waitlist = db.session.query(Waitlist).filter_by(status='waiting').order_by(Waitlist.created_at.desc()).limit(10).all()
    recent_appointments = []
    for a in recent_appointments_raw:
        student = User.query.get(a.student_id)
        recent_appointments.append({
            "time": a.time,
            "status": a.status,
            "student_name": student.name if student else "Unknown"
        })

    monthly_data = db.session.query(
        func.strftime('%Y-%m', Appointment.time).label('month'),
        func.count(Appointment.id)
    ).group_by('month').order_by('month').all()
    months = [row[0] for row in monthly_data]
    counts = [row[1] for row in monthly_data]

    advisor_data = db.session.query(
        User.name,
        func.count(Appointment.id)
    ).join(Appointment, Appointment.advisor_id == User.id)\
     .group_by(User.id)\
     .order_by(func.count(Appointment.id).desc())\
     .limit(5).all()
    advisor_names = [row[0] for row in advisor_data]
    advisor_counts = [row[1] for row in advisor_data]

    total_this_month = Appointment.query.filter(func.strftime('%Y-%m', Appointment.time) == current_month).count()
    total_completed = Appointment.query.filter_by(status='completed').count()
    total_noshow = Appointment.query.filter_by(status='no-show').count()
    
    cancel_labels = ['Conflict', 'Sick', 'Forgot', 'Other']
    cancel_counts = [15, 8, 5, 12]

    return render_template("dashboard.html",
    months=months,
    counts=counts,
    advisor_names=advisor_names,
    advisor_counts=advisor_counts,
    total_this_month=total_this_month,
    total_completed=total_completed,
    total_noshow=total_noshow,
    cancel_labels=cancel_labels,
    cancel_counts=cancel_counts,
    recent_appointments=recent_appointments, 
    recent_waitlist=recent_waitlist
)

    
