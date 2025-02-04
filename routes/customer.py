from flask import Blueprint, request, jsonify
from app import db
from models import User, ServiceRequest, Review, Service
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from functools import wraps

customer_bp = Blueprint('customer', __name__)

def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or current_user.role != 'customer':
            return jsonify({'error': 'Customer access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@customer_bp.route('/service-request', methods=['POST'])
@jwt_required()
@customer_required
def create_service_request():
    data = request.get_json()
    current_user = User.query.get(get_jwt_identity())
    
    service = Service.query.get(data['service_id'])
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    
    service_request = ServiceRequest(
        customer_id=current_user.id,
        service_id=data['service_id'],
        description=data['description'],
        preferred_date=datetime.strptime(data['preferred_date'], '%Y-%m-%d').date(),
        preferred_time=data['preferred_time'],
        address=data['address'],
        pin_code=data['pin_code']
    )
    
    db.session.add(service_request)
    db.session.commit()
    
    return jsonify({
        'message': 'Service request created successfully',
        'request_id': service_request.id
    }), 201

@customer_bp.route('/service-requests', methods=['GET'])
@jwt_required()
@customer_required
def get_service_requests():
    current_user = User.query.get(get_jwt_identity())
    requests = ServiceRequest.query.filter_by(customer_id=current_user.id).all()
    
    return jsonify([{
        'id': req.id,
        'service_id': req.service_id,
        'status': req.status,
        'preferred_date': req.preferred_date.strftime('%Y-%m-%d'),
        'preferred_time': req.preferred_time,
        'created_at': req.created_at.isoformat()
    } for req in requests]), 200

@customer_bp.route('/service-requests/<int:request_id>', methods=['GET'])
@jwt_required()
@customer_required
def get_service_request(request_id):
    current_user = User.query.get(get_jwt_identity())
    request = ServiceRequest.query.filter_by(
        id=request_id, 
        customer_id=current_user.id
    ).first()
    
    if not request:
        return jsonify({'error': 'Service request not found'}), 404
    
    return jsonify({
        'id': request.id,
        'service_id': request.service_id,
        'status': request.status,
        'preferred_date': request.preferred_date.strftime('%Y-%m-%d'),
        'preferred_time': request.preferred_time,
        'professional_id': request.professional_id,
        'created_at': request.created_at.isoformat()
    }), 200

@customer_bp.route('/reviews', methods=['POST'])
@jwt_required()
@customer_required
def submit_review():
    data = request.get_json()
    current_user = User.query.get(get_jwt_identity())
    
    service_request = ServiceRequest.query.filter_by(
        id=data['service_request_id'],
        customer_id=current_user.id,
        status='completed'
    ).first()
    
    if not service_request:
        return jsonify({'error': 'Service request not found or not completed'}), 404
    
    review = Review(
        service_request_id=service_request.id,
        rating=data['rating'],
        comment=data.get('comment'),
        punctuality=data['aspects']['punctuality'],
        professionalism=data['aspects']['professionalism'],
        work_quality=data['aspects']['work_quality']
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({'message': 'Review submitted successfully'}), 201