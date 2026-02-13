"""
User service - Handles user-related operations

Business logic for:
- Getting user profile
- Updating user profile
- User account management
"""

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from database import db
from models import User
from utils.security import hash_password
from exceptions import (
    UserNotFoundError,
    DuplicateUserError,
    DatabaseError
)


class UserService:
    """Service for user operations"""
    
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User object
            
        Raises:
            UserNotFoundError: If user doesn't exist
        """
        user = db.session.get(User, user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user
    
    @staticmethod
    def get_user_by_username(username: str) -> User:
        """
        Get user by username
        
        Args:
            username: Username
            
        Returns:
            User object
            
        Raises:
            UserNotFoundError: If user doesn't exist
        """
        user = User.query.filter_by(username=username.lower()).first()
        if not user:
            raise UserNotFoundError()
        return user
    
    @staticmethod
    def update_user(user_id: int, email: str = None, password: str = None) -> User:
        """
        Update user profile
        
        Args:
            user_id: User ID
            email: New email (optional)
            password: New password (optional)
            
        Returns:
            Updated User object
            
        Raises:
            UserNotFoundError: If user doesn't exist
            DuplicateUserError: If email already exists
            DatabaseError: If database operation fails
        """
        user = UserService.get_user_by_id(user_id)
        
        try:
            # Update email if provided
            if email:
                # Check if email is already taken by another user
                existing = User.query.filter(
                    User.email == email.lower(),
                    User.id != user_id
                ).first()
                
                if existing:
                    raise DuplicateUserError('email', email)
                
                user.email = email.lower()
            
            # Update password if provided
            if password:
                user.password_hash = hash_password(password)
            
            db.session.commit()
            return user
            
        except IntegrityError as e:
            db.session.rollback()
            if 'email' in str(e).lower():
                raise DuplicateUserError('email', email)
            else:
                raise DatabaseError(f"Failed to update user: {str(e)}")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(f"Failed to update user: {str(e)}")
    
    @staticmethod
    def deactivate_user(user_id: int) -> User:
        """
        Deactivate user account
        
        Args:
            user_id: User ID
            
        Returns:
            Updated User object
            
        Raises:
            UserNotFoundError: If user doesn't exist
            DatabaseError: If database operation fails
        """
        user = UserService.get_user_by_id(user_id)
        
        try:
            user.is_active = False
            db.session.commit()
            return user
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(f"Failed to deactivate user: {str(e)}")
