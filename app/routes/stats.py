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
