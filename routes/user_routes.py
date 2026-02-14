"""
User routes - User profile management

Endpoints:
- GET /users/me - Get current user profile
- PUT /users/me - Update current user profile
"""

from flask import Blueprint, request
from pydantic import ValidationError as PydanticValidationError

from services import UserService
from schemas import UserResponse, UserUpdate
from utils import create_success_response, create_error_response
from middleware import jwt_required, get_current_user
from config import (
    AuthenticationError,
    DuplicateUserError,
    DatabaseError
)

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/me', methods=['GET'])
@jwt_required
def get_profile():
    """
    Get current user profile
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: User profile
        401: Unauthorized
    """
    try:
        user = get_current_user()
        return create_success_response(
            data=UserResponse.model_validate(user)
        )
        
    except AuthenticationError as e:
        return create_error_response(str(e), 401)


@users_bp.route('/me', methods=['PUT'])
@jwt_required
def update_profile():
    """
    Update current user profile
    
    Headers:
        Authorization: Bearer <access_token>
    
    Request body (all optional):
        {
            "email": "newemail@example.com",
            "password": "NewSecurePass123!"
        }
    
    Returns:
        200: Updated profile
        400: Validation error
        401: Unauthorized
    """
    if not request.is_json:
        return create_error_response("Content-Type must be application/json", 400)
    
    try:
        user = get_current_user()
        
        # Validate request
        schema = UserUpdate(**request.get_json())
        
        # Update user
        updated_user = UserService.update_user(
            user_id=user.id,
            email=schema.email,
            password=schema.password
        )
        
        return create_success_response(
            data=UserResponse.model_validate(updated_user),
            message="Profile updated successfully"
        )
        
    except PydanticValidationError as e:
        errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        return create_error_response("; ".join(errors), 400)
    except DuplicateUserError as e:
        return create_error_response(str(e), 400)
    except AuthenticationError as e:
        return create_error_response(str(e), 401)
    except DatabaseError as e:
        return create_error_response(str(e), 500)
