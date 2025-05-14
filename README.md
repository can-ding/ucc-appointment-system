# 🗓️ UCC Appointment Management System

A lightweight appointment management platform for university career center (UCC) staff and students. Built with **Flask**, this system enables appointment tracking, waitlist management, and real-time statistics for admin and student users.

---

## 🔍 Features

### ✅ Admin Dashboard
- 📊 Real-time statistics: total, completed, no-show appointments
- 📈 Monthly appointment trend chart
- 🧑‍🏫 Top advisors ranking (pie chart)
- ❌ Cancellation reasons (doughnut chart)
- 📄 Recent appointments & waitlist preview
- 📥 One-click CSV export of appointment and waitlist records

### ✅ Student Portal
- 📅 Book an appointment (UI structure ready)
- 📖 View current & past appointments
- 🔔 Cancel appointment with reason (modal ready)
- 🕒 Join waitlist if preferred time is fully booked

---

## 💡 Tech Stack

- **Backend**: Flask + SQLAlchemy + SQLite
- **Frontend**: Bootstrap 5 + Jinja2 Templates + Chart.js
- **Deployment**: [Render](https://render.com) (gunicorn)
- **Session Ready**: Blueprint structure, future support for auth & login

---

## 🔐 Coming Soon (Planned Features)

- 👥 User login system (student/admin login page with session control)
- 🔐 Route-based permission handling
- 📧 Email reminders or notifications
- 🗂️ Advisor management (CRUD for advisors)
- 🌐 Improved mobile responsiveness

---

## 🚀 Deployment

Currently live on Render:  
👉 [Live Demo Link](https://your-site-name.onrender.com) ← *(replace with your actual link)*

> ⚙️ To deploy it yourself:
> 1. Push to GitHub
> 2. Add `render.yaml`, `Procfile`, and `requirements.txt`  
> 3. Deploy via [Render.com](https://render.com) using Gunicorn  
> 4. Done!

---

## 🧪 Local Development

```bash
# Clone the project
git clone https://github.com/your-username/ucc-appointment-system.git

# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python run.py
