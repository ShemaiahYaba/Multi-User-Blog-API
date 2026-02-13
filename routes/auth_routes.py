"""
Authentication routes - Register, Login, Refresh Token

Endpoints:
- POST /auth/register - Create new user account
- POST /auth/login - Login and get JWT tokens  
- POST /auth/refresh - Get new access token using refresh token
"""

from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from pydantic import ValidationError as PydanticValidationError

from services import AuthService, UserService
from schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from utils import create_success_response, create_error_response
from exceptions import (
    AuthenticationError,
    DuplicateUserError,
    DatabaseError,
    ValidationError
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request body:
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "SecurePass123!"
        }
    
    Returns:
        201: User created with tokens
        400: Validation error or duplicate user
    """
    if not request.is_json:
        return create_error_response("Content-Type must be application/json", 400)
    
    try:
        # Validate request with Pydantic
        schema = UserRegister(**request.get_json())
        
        # Register user
        user = AuthService.register_user(
            username=schema.username,
            email=schema.email,
            password=schema.password
        )
        
        # Create JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        # Build response
        response_data = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=900,  # 15 minutes
            user=UserResponse.model_validate(user)
        )
        
        return create_success_response(
            data=response_data,
            message="User registered successfully",
            status_code=201
        )
        
    except PydanticValidationError as e:
        # Pydantic validation errors
        errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        return create_error_response("; ".join(errors), 400)
    except DuplicateUserError as e:
        return create_error_response(str(e), 400)
    except DatabaseError as e:
        return create_error_response(str(e), 500)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT tokens
    
    Request body:
        {
            "username": "john_doe",  # or email
            "password": "SecurePass123!"
        }
    
    Returns:
        200: Login successful with tokens
        401: Invalid credentials
    """
    if not request.is_json:
        return create_error_response("Content-Type must be application/json", 400)
    
    try:
        # Validate request
        schema = UserLogin(**request.get_json())
        
        # Authenticate user
        user = AuthService.authenticate_user(
            username=schema.username,
            password=schema.password
        )
        
        # Create JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        # Build response
        response_data = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=900,  # 15 minutes
            user=UserResponse.model_validate(user)
        )
        
        return create_success_response(data=response_data)
        
    except PydanticValidationError as e:
        errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        return create_error_response("; ".join(errors), 400)
    except AuthenticationError as e:
        return create_error_response(str(e), 401)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Get new access token using refresh token
    
    Headers:
        Authorization: Bearer <refresh_token>
    
    Returns:
        200: New access token
        401: Invalid or expired refresh token
    """
    try:
        # Get user ID from refresh token
        user_id = get_jwt_identity()
        
        # Verify user still exists and is active
        user = UserService.get_user_by_id(user_id)
        
        if not user.is_active:
            return create_error_response("Account is inactive", 401)
        
        # Create new access token
        access_token = create_access_token(identity=user_id)
        
        return create_success_response(
            data={
                'access_token': access_token,
                'token_type': 'Bearer',
                'expires_in': 900
            }
        )
        
    except Exception as e:
        return create_error_response("Invalid or expired refresh token", 401)
