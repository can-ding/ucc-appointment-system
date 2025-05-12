from flask import Flask
from app.extensions import db 
from app.models.appointment import Appointment
from app.routes.main import main_bp
from app.routes.user import user_bp
from app.routes.appointment import appointment_bp
from app.routes.stats import stats_bp

blueprints = [main_bp, user_bp, appointment_bp, stats_bp]

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    

    for bp in blueprints:
        app.register_blueprint(bp)

    return app

