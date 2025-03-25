from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Service, ServiceRequest
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from sqlalchemy import func
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or current_user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_stats():
    pending_professionals = User.query.filter_by(role='professional', is_approved=False).count()
    total_services = Service.query.count()
    active_requests = ServiceRequest.query.filter(ServiceRequest.status.in_(['pending', 'accepted'])).count()
    
    return jsonify({
        'pendingProfessionals': pending_professionals,
        'totalServices': total_services,
        'activeRequests': active_requests
    }), 200

@admin_bp.route('/recent-requests', methods=['GET'])
@jwt_required()
@admin_required
def get_recent_requests():
    recent = ServiceRequest.query.join(Service).order_by(ServiceRequest.created_at.desc()).limit(10).all()
    return jsonify([{
        'id': req.id,
        'service_name': Service.query.get(req.service_id).name,
        'status': req.status,
        'created_at': req.created_at.isoformat()
    } for req in recent]), 200

@admin_bp.route('/service-performance', methods=['GET'])
@jwt_required()
@admin_required
def get_service_performance():
    last_month = datetime.utcnow() - timedelta(days=30)
    performance = db.session.query(
        Service.category,
        func.count(ServiceRequest.id)
    ).join(ServiceRequest).filter(
        ServiceRequest.status == 'completed',
        ServiceRequest.completed_at >= last_month
    ).group_by(Service.category).all()
    
    categories = ['Plumbing', 'Electrical', 'Cleaning', 'Carpentry', 'Painting']
    performance_dict = dict(performance)
    
    return jsonify([performance_dict.get(cat, 0) for cat in categories]), 200

@admin_bp.route('/professionals/pending', methods=['GET'])
@jwt_required()
@admin_required
def get_pending_professionals():
    professionals = User.query.filter_by(role='professional', is_approved=False).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'email': p.email,
        'service_type': p.service_type,
        'experience': p.experience,
        'description': p.description
    } for p in professionals]), 200

@admin_bp.route('/professionals/<int:id>/approve', methods=['POST'])
@jwt_required()
@admin_required
def approve_professional(id):
    professional = User.query.filter_by(id=id, role='professional').first()
    if not professional:
        return jsonify({'error': 'Professional not found'}), 404
    
    professional.is_approved = True
    db.session.commit()
    
    return jsonify({'message': 'Professional approved successfully'}), 200

@admin_bp.route('/services', methods=['POST'])
@jwt_required()
@admin_required
def create_service():
    data = request.get_json()
    
    required_fields = ['name', 'description', 'category', 'base_price', 'required_time']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    valid_categories = ['Plumbing', 'Electrical', 'Cleaning', 'Carpentry', 'Painting']
    if data['category'] not in valid_categories:
        return jsonify({'error': 'Invalid category'}), 400
    
    try:
        base_price = float(data['base_price'])
        if base_price <= 0:
            return jsonify({'error': 'Base price must be greater than 0'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid base price'}), 400
    
    try:
        required_time = int(data['required_time'])
        if required_time <= 0:
            return jsonify({'error': 'Required time must be greater than 0'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid required time'}), 400
    
    service = Service(
        name=data['name'],
        description=data['description'],
        category=data['category'],
        base_price=base_price,
        required_time=required_time
    )
    
    db.session.add(service)
    db.session.commit()
    
    return jsonify({
        'message': 'Service created successfully',
        'service': {
            'id': service.id,
            'name': service.name,
            'category': service.category,
            'base_price': service.base_price,
            'required_time': service.required_time
        }
    }), 201