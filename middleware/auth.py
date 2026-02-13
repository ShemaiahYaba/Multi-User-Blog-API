"""
Authentication middleware - JWT decorators and helpers

Provides:
- @jwt_required decorator for protected routes
- @admin_required decorator for admin-only routes
- Helper functions to get current user
"""

from functools import wraps
from flask import request
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity,
    get_jwt
)
from models import User
from exceptions import AuthenticationError, AuthorizationError, UserNotFoundError


def get_current_user() -> User:
    """
    Get the current authenticated user from JWT
    
    Returns:
        User object
        
    Raises:
        AuthenticationError: If no valid JWT or user not found
    """
    try:
        # Verify JWT exists
        verify_jwt_in_request()
        
        # Get user ID from JWT
        user_id = get_jwt_identity()
        
        # Fetch user from database
        from database import db
        user = db.session.get(User, user_id)
        
        if not user:
            raise UserNotFoundError(user_id)
        
        if not user.is_active:
            raise AuthenticationError("Account is inactive")
        
        return user
        
    except Exception as e:
        if isinstance(e, (AuthenticationError, UserNotFoundError)):
            raise
        raise AuthenticationError("Invalid or expired token")


def get_current_user_id() -> int:
    """
    Get current user ID from JWT
    
    Returns:
        User ID as integer
        
    Raises:
        AuthenticationError: If no valid JWT
    """
    try:
        verify_jwt_in_request()
        return int(get_jwt_identity())
    except Exception:
        raise AuthenticationError("Invalid or expired token")


def jwt_required(fn):
    """
    Decorator to protect routes - requires valid JWT
    
    Usage:
        @app.route('/protected')
        @jwt_required
        def protected_route():
            user = get_current_user()
            return {'message': f'Hello {user.username}'}
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            raise AuthenticationError("Authentication required")
    
    return wrapper


def admin_required(fn):
    """
    Decorator to protect admin-only routes
    
    Requires valid JWT AND admin role.
    
    Usage:
        @app.route('/admin')
        @admin_required
        def admin_route():
            return {'message': 'Admin access granted'}
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Verify JWT
            verify_jwt_in_request()
            
            # Get current user
            user = get_current_user()
            
            # Check if admin
            if not user.is_admin():
                raise AuthorizationError("Admin access required")
            
            return fn(*args, **kwargs)
            
        except AuthorizationError:
            raise
        except Exception as e:
            raise AuthenticationError("Authentication required")
    
    return wrapper


def optional_jwt(fn):
    """
    Decorator for routes that work with or without JWT
    
    If JWT is present and valid, user info will be available.
    If not, the route still works but user will be None.
    
    Usage:
        @app.route('/optional')
        @optional_jwt
        def optional_route():
            try:
                user = get_current_user()
                return {'message': f'Hello {user.username}'}
            except:
                return {'message': 'Hello guest'}
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
        except:
            pass  # Ignore JWT errors for optional routes
        
        return fn(*args, **kwargs)
    
    return wrapper
