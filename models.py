from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, customer, professional
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Professional specific fields
    service_type = db.Column(db.String(100))
    experience = db.Column(db.Integer)
    description = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)
    
    # Customer specific fields
    pin_code = db.Column(db.String(10))

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    required_time = db.Column(db.Integer, nullable=False)  # in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, completed, cancelled
    description = db.Column(db.Text, nullable=False)
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.String(5), nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    completion_notes = db.Column(db.Text)
    duration = db.Column(db.Integer)  # actual duration in minutes

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    punctuality = db.Column(db.Integer)
    professionalism = db.Column(db.Integer)
    work_quality = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)