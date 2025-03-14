from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from extensions import db, migrate, jwt, bcrypt, limiter
from models import User, Service, ServiceRequest, Review

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure Flask app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)
    limiter.init_app(app)
    
    # Import routes
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.customer import customer_bp
    from routes.professional import professional_bp
    from routes.service import service_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(customer_bp, url_prefix='/customer')
    app.register_blueprint(professional_bp, url_prefix='/professional')
    app.register_blueprint(service_bp, url_prefix='/services')
    
    # Error handling
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request', 'message': str(error)}, 400

    @app.errorhandler(401)
    def unauthorized(error):
        return {'error': 'Unauthorized', 'message': 'Invalid or missing token'}, 401

    @app.errorhandler(403)
    def forbidden(error):
        return {'error': 'Forbidden', 'message': 'Insufficient permissions'}, 403

    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found', 'message': 'Resource not found'}, 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return {'error': 'Internal server error', 'message': 'An unexpected error occurred'}, 500

    # Create admin user
    @app.before_first_request
    def create_admin():
        with app.app_context():
            admin = User.query.filter_by(email='admin@example.com').first()
            if not admin:
                admin = User(
                    email='admin@example.com',
                    password=bcrypt.generate_password_hash('Admin@123').decode('utf-8'),
                    name='Admin',
                    role='admin'
                )
                db.session.add(admin)
                db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)