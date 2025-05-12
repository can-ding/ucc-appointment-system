from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User 

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    role = data.get('role')

    if not all([name, email, role]):
        return jsonify({'error': 'Missing fields'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    new_user = User(name=name, email=email, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created', 'user_id': new_user.id}), 201
