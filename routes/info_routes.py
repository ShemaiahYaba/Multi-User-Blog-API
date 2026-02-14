"""
Info routes - API information and health check

Endpoints:
- GET / - API documentation
- GET /health - Health check
"""

from flask import Blueprint, jsonify
from db import db

info_bp = Blueprint('info', __name__)


@info_bp.route('/', methods=['GET'])
def home():
    """API information and documentation"""
    return jsonify({
        'message': 'Blog API with Authentication',
        'version': '1.0.0',
        'features': [
            'User registration and authentication',
            'JWT access and refresh tokens',
            'Role-based access control (User, Admin)',
            'Blog post CRUD operations',
            'Ownership-based authorization',
            'Pydantic schema validation',
            'Database constraints',
            'Comprehensive security'
        ],
        'endpoints': {
            'auth': {
                'POST /auth/register': 'Register new user',
                'POST /auth/login': 'Login and get tokens',
                'POST /auth/refresh': 'Refresh access token'
            },
            'users': {
                'GET /users/me': 'Get current user profile (auth required)',
                'PUT /users/me': 'Update profile (auth required)'
            },
            'posts': {
                'GET /posts': 'List all posts (public)',
                'GET /posts/:id': 'Get specific post (public)',
                'POST /posts': 'Create post (auth required)',
                'PUT /posts/:id': 'Update own post (auth required)',
                'DELETE /posts/:id': 'Delete own post or any post if admin (auth required)'
            }
        },
        'authentication': {
            'type': 'JWT (JSON Web Token)',
            'header': 'Authorization: Bearer <token>',
            'access_token_expires': '15 minutes',
            'refresh_token_expires': '7 days'
        },
        'authorization': {
            'user': 'Can CRUD own posts',
            'admin': 'Can delete any post'
        }
    }), 200


@info_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Tests database connectivity.
    """
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500
