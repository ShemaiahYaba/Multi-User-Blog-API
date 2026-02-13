"""
Routes package - Flask blueprints for all API endpoints
"""

from .auth_routes import auth_bp
from .user_routes import users_bp
from .post_routes import posts_bp
from .info_routes import info_bp

__all__ = ['auth_bp', 'users_bp', 'posts_bp', 'info_bp']
