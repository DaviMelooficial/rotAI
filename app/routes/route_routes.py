from flask import Blueprint, jsonify, request
from ..models import Route, db
from ..services.ia_service import generate_route

route_bp = Blueprint('route', __name__)

@route_bp.route('/api/route', methods=['POST'])
def create_route():
    data = request.get_json()
    user_id = data.get('user_id')
    route_data = generate_route(user_id)
    
    new_route = Route(user_id=user_id, points=route_data['points'], total_cost=route_data['total_cost'])
    db.session.add(new_route)
    db.session.commit()
    
    return jsonify({'message': 'Route created successfully', 'route_id': new_route.id}), 201
