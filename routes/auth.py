from flask import Blueprint, request, jsonify
from app import db, bcrypt
from models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'role': user.role
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/register/customer', methods=['POST'])
def register_customer():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    customer = User(
        email=data['email'],
        password=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
        name=data['name'],
        role='customer',
        pin_code=data['pin_code']
    )
    
    db.session.add(customer)
    db.session.commit()
    
    return jsonify({'message': 'Customer registered successfully'}), 201

@auth_bp.route('/register/professional', methods=['POST'])
def register_professional():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    professional = User(
        email=data['email'],
        password=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
        name=data['name'],
        role='professional',
        service_type=data['service_type'],
        experience=data['experience'],
        description=data['description'],
        is_approved=False
    )
    
    db.session.add(professional)
    db.session.commit()
    
    return jsonify({'message': 'Professional registered successfully'}), 201