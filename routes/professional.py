from flask import Blueprint, request, jsonify
from app import db
from models import User, ServiceRequest, Review, Service
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from functools import wraps

professional_bp = Blueprint('professional', __name__)

def professional_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or current_user.role != 'professional' or not current_user.is_approved:
            return jsonify({'error': 'Approved professional access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@professional_bp.route('/requests', methods=['GET'])
@jwt_required()
@professional_required
def get_available_requests():
    current_user = User.query.get(get_jwt_identity())
    
    # Get requests matching professional's service type and location
    requests = ServiceRequest.query.join(Service).filter(
        ServiceRequest.status == 'pending',
        Service.category == current_user.service_type
    ).all()
    
    return jsonify([{
        'id': req.id,
        'service_id': req.service_id,
        'description': req.description,
        'preferred_date': req.preferred_date.strftime('%Y-%m-%d'),
        'preferred_time': req.preferred_time,
        'pin_code': req.pin_code
    } for req in requests]), 200

@professional_bp.route('/requests/<int:request_id>/accept', methods=['POST'])
@jwt_required()
@professional_required
def accept_request(request_id):
    current_user = User.query.get(get_jwt_identity())
    request = ServiceRequest.query.filter_by(id=request_id, status='pending').first()
    
    if not request:
        return jsonify({'error': 'Service request not found or not pending'}), 404
    
    request.professional_id = current_user.id
    request.status = 'accepted'
    db.session.commit()
    
    return jsonify({'message': 'Service request accepted successfully'}), 200

@professional_bp.route('/requests/<int:request_id>/complete', methods=['POST'])
@jwt_required()
@professional_required
def complete_request(request_id):
    data = request.get_json()
    current_user = User.query.get(get_jwt_identity())
    
    service_request = ServiceRequest.query.filter_by(
        id=request_id,
        professional_id=current_user.id,
        status='accepted'
    ).first()
    
    if not service_request:
        return jsonify({'error': 'Service request not found or not accepted'}), 404
    
    service_request.status = 'completed'
    service_request.completed_at = datetime.utcnow()
    service_request.completion_notes = data.get('notes')
    service_request.duration = data.get('duration')
    
    db.session.commit()
    
    return jsonify({'message': 'Service request completed successfully'}), 200

@professional_bp.route('/reviews', methods=['GET'])
@jwt_required()
@professional_required
def get_reviews():
    current_user = User.query.get(get_jwt_identity())
    
    reviews = Review.query.join(ServiceRequest).filter(
        ServiceRequest.professional_id == current_user.id
    ).all()
    
    return jsonify([{
        'id': review.id,
        'service_request_id': review.service_request_id,
        'rating': review.rating,
        'comment': review.comment,
        'aspects': {
            'punctuality': review.punctuality,
            'professionalism': review.professionalism,
            'work_quality': review.work_quality
        },
        'created_at': review.created_at.isoformat()
    } for review in reviews]), 200