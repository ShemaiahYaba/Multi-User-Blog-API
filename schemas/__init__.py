"""
Schemas package - Pydantic models for validation and serialization

Separates API contract (schemas) from database models.
"""

from .user import UserRegister, UserLogin, UserResponse, UserUpdate, UserBrief
from .post import PostCreate, PostUpdate, PostResponse, PostBrief
from .auth import TokenResponse, RefreshTokenRequest
from .common import PaginatedResponse, MessageResponse

__all__ = [
    'UserRegister', 'UserLogin', 'UserResponse', 'UserUpdate', 'UserBrief',
    'PostCreate', 'PostUpdate', 'PostResponse', 'PostBrief',
    'TokenResponse', 'RefreshTokenRequest',
    'PaginatedResponse', 'MessageResponse'
]
