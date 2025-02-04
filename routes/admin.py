from flask import Blueprint, request, jsonify
from app import db
from models import User, Service
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or current_user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/professionals/pending', methods=['GET'])
@jwt_required()
@admin_required
def get_pending_professionals():
    professionals = User.query.filter_by(role='professional', is_approved=False).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'service_type': p.service_type,
        'experience': p.experience
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
    
    service = Service(
        name=data['name'],
        description=data['description'],
        category=data['category'],
        base_price=data['base_price'],
        required_time=data['required_time']
    )
    
    db.session.add(service)
    db.session.commit()
    
    return jsonify({
        'message': 'Service created successfully',
        'service_id': service.id
    }), 201