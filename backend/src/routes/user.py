# src/routes/user.py
from flask import Blueprint, request, jsonify
from src.models.user import User # Import User model
from src.models import db # Import db from src.models package

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Add other user-related routes here
