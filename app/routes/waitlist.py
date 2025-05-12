from flask import Blueprint, request, jsonify, render_template
from app.extensions import db
from app.models.waitlist import Waitlist
from datetime import datetime

waitlist_bp = Blueprint("waitlist", __name__, url_prefix="/waitlist")

# API endpoint: join the waitlist
@waitlist_bp.route("/join", methods=["POST"])
def join_waitlist():
    data = request.get_json()
    student_name = data.get("student_name")
    student_email = data.get("student_email")
    advisor_id = data.get("advisor_id")
    time_str = data.get("desired_time")

    if not all([student_name, student_email, advisor_id, time_str]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        desired_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({"error": "Invalid time format. Use YYYY-MM-DD HH:MM"}), 400

    new_wait = Waitlist(
        student_name=student_name,
        student_email=student_email,
        advisor_id=advisor_id,
        desired_time=desired_time
    )
    db.session.add(new_wait)
    db.session.commit()

    return jsonify({"message": "Joined waitlist successfully"}), 201

# Web page: view waitlist entries
@waitlist_bp.route("", methods=["GET"])
def view_waitlist():
    entries = Waitlist.query.filter_by(status='waiting').order_by(Waitlist.created_at).all()
    data = []
    for entry in entries:
        data.append({
            "id": entry.id,
            "student": entry.student_name,
            "email": entry.student_email,
            "advisor_id": entry.advisor_id,
            "time": entry.desired_time.strftime("%Y-%m-%d %H:%M"),
            "status": entry.status
        })
    return render_template("waitlist.html", waitlist=data)

# Demo: simple test page
@waitlist_bp.route("/demo")
def waitlist_demo():
    return render_template("waitlist_demo.html")
