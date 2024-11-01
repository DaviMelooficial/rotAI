from flask import Blueprint, request, jsonify
from ..models import User, db
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/user', methods=['POST'])
def create_user():
    data = request.get_json()
    location = data.get('location')
    budget = data.get('budget')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d')
    
    new_user = User(location=location, budget=budget, date=date)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201
