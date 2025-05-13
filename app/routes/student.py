from flask import Blueprint, render_template

student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.route("/")
def home():
    return render_template("student_home.html")

@student_bp.route("/book")
def book():
    return render_template("student_book.html")

@student_bp.route("/my")
def my_appointments():
    return render_template("student_appointments.html")

@student_bp.route("/waitlist")
def waitlist():
    return render_template("student_waitlist.html")
