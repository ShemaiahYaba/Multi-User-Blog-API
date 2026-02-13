"""
Blog API with Authentication - Week 4 Project
Backend Engineering Fundamentals

A production-ready blog API featuring:
- User authentication with JWT
- Role-based access control
- Pydantic schema validation
- Database constraints
- Comprehensive testing
- Clean architecture
"""

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

from config import get_config
from database import init_db
from routes import auth_bp, users_bp, posts_bp, info_bp
from utils import create_error_response


def create_app():
    """
    Application factory
    
    Creates and configures the Flask application with all extensions,
    blueprints, and error handlers.
    
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(get_config())
    
    # Initialize extensions
    init_db(app)
    jwt = JWTManager(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    app.register_blueprint(info_bp)        # / and /health
    app.register_blueprint(auth_bp)        # /auth/*
    app.register_blueprint(users_bp)       # /users/*
    app.register_blueprint(posts_bp)       # /posts/*
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return create_error_response("Token has expired", 401)
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return create_error_response("Invalid token", 401)
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return create_error_response("Authorization required", 401)
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return create_error_response("Resource not found", 404)
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return create_error_response("Method not allowed", 405)
    
    @app.errorhandler(500)
    def internal_error(error):
        return create_error_response("Internal server error", 500)
    
    return app


def print_startup_info(app):
    """Print startup information"""
    print("\n" + "="*70)
    print("🚀 Blog API with Authentication (Week 4)")
    print("="*70)
    print(f"📊 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"🌐 Server: http://localhost:{os.environ.get('PORT', 5000)}")
    print(f"🔧 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print("\n✨ Features:")
    print("  • JWT Authentication (access + refresh tokens)")
    print("  • Role-based Access Control (user, admin)")
    print("  • Pydantic Schema Validation")
    print("  • Database Constraints")
    print("  • Password Hashing (bcrypt)")
    print("  • Ownership-based Authorization")
    print("\n📁 Clean Architecture:")
    print("  • models/ - SQLAlchemy ORM with constraints")
    print("  • schemas/ - Pydantic validation")
    print("  • services/ - Business logic")
    print("  • middleware/ - JWT decorators")
    print("  • routes/ - Flask blueprints")
    print("  • utils/ - Helper functions")
    print("\n🔐 Security:")
    print("  • Passwords never stored in plain text")
    print("  • SQL injection prevention (SQLAlchemy)")
    print("  • Input validation (Pydantic)")
    print("  • CORS configuration")
    print("  • Token expiration")
    print("="*70 + "\n")


if __name__ == '__main__':
    # Create application
    app = create_app()
    
    # Print startup info
    print_startup_info(app)
    
    # Run application
    port = int(os.environ.get('PORT', 5000))
    debug = app.config['DEBUG']
    
    app.run(host='0.0.0.0', port=port, debug=debug)
