from flask import Blueprint, request, jsonify
from app import db, bcrypt
from models import User
from flask_jwt_extended import create_access_token
from email_validator import validate_email, EmailNotValidError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400
    
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
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['email', 'password', 'name', 'pin_code']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        validate_email(data['email'])
    except EmailNotValidError:
        return jsonify({'error': 'Invalid email format'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    if not data['pin_code'].isdigit() or len(data['pin_code']) != 6:
        return jsonify({'error': 'PIN code must be 6 digits'}), 400
    
    try:
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
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500

@auth_bp.route('/register/professional', methods=['POST'])
def register_professional():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['email', 'password', 'name', 'service_type', 'experience', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        validate_email(data['email'])
    except EmailNotValidError:
        return jsonify({'error': 'Invalid email format'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    valid_service_types = ['Plumbing', 'Electrical', 'Cleaning', 'Carpentry', 'Painting']
    if data['service_type'] not in valid_service_types:
        return jsonify({'error': 'Invalid service type'}), 400
    
    try:
        experience = int(data['experience'])
        if experience < 0:
            return jsonify({'error': 'Experience must be a positive number'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Experience must be a valid number'}), 400
    
    try:
        professional = User(
            email=data['email'],
            password=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
            name=data['name'],
            role='professional',
            service_type=data['service_type'],
            experience=experience,
            description=data['description'],
            is_approved=False
        )
        
        db.session.add(professional)
        db.session.commit()
        
        return jsonify({'message': 'Professional registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500