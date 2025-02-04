from flask import Blueprint, request, jsonify
from app import db
from models import Service, Review, ServiceRequest
from flask_jwt_extended import jwt_required
from sqlalchemy import func

service_bp = Blueprint('service', __name__)

@service_bp.route('', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'description': s.description,
        'category': s.category,
        'base_price': s.base_price,
        'required_time': s.required_time
    } for s in services]), 200

@service_bp.route('/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    
    # Calculate average rating
    avg_rating = db.session.query(func.avg(Review.rating)).join(ServiceRequest).filter(
        ServiceRequest.service_id == service_id
    ).scalar() or 0
    
    return jsonify({
        'id': service.id,
        'name': service.name,
        'description': service.description,
        'category': service.category,
        'base_price': service.base_price,
        'required_time': service.required_time,
        'average_rating': float(avg_rating)
    }), 200

@service_bp.route('/search', methods=['GET'])
def search_services():
    query = request.args.get('q', '')
    pin_code = request.args.get('pin_code')
    category = request.args.get('category')
    
    services_query = Service.query
    
    if query:
        services_query = services_query.filter(
            Service.name.ilike(f'%{query}%') | 
            Service.description.ilike(f'%{query}%')
        )
    
    if category:
        services_query = services_query.filter(Service.category == category)
    
    services = services_query.all()
    
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'description': s.description,
        'category': s.category,
        'base_price': s.base_price,
        'required_time': s.required_time
    } for s in services]), 200