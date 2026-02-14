"""
Authentication service - Handles user registration and login

Business logic for:
- User registration
- User login
- Password verification
"""

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db import db
from models import User
from utils.security import hash_password, verify_password
from config import (
    AuthenticationError,
    DuplicateUserError,
    DatabaseError
)


class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def register_user(username: str, email: str, password: str, role: str = 'user') -> User:
        """
        Register a new user
        
        Args:
            username: Unique username
            email: Unique email address
            password: Plain text password (will be hashed)
            role: User role (default: 'user')
            
        Returns:
            Created User object
            
        Raises:
            DuplicateUserError: If username or email already exists
            DatabaseError: If database operation fails
        """
        # Check if username exists
        existing_user = User.query.filter_by(username=username.lower()).first()
        if existing_user:
            raise DuplicateUserError('username', username)
        
        # Check if email exists
        existing_email = User.query.filter_by(email=email.lower()).first()
        if existing_email:
            raise DuplicateUserError('email', email)
        
        try:
            # Hash password
            password_hash = hash_password(password)
            
            # Create user
            user = User(
                username=username.lower(),
                email=email.lower(),
                password_hash=password_hash,
                role=role,
                is_active=True
            )
            
            db.session.add(user)
            db.session.commit()
            
            return user
            
        except IntegrityError as e:
            db.session.rollback()
            # Database constraint violation
            if 'username' in str(e).lower():
                raise DuplicateUserError('username', username)
            elif 'email' in str(e).lower():
                raise DuplicateUserError('email', email)
            else:
                raise DatabaseError(f"Failed to create user: {str(e)}")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(f"Failed to create user: {str(e)}")
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> User:
        """
        Authenticate user with username/email and password
        
        Args:
            username: Username or email
            password: Plain text password
            
        Returns:
            User object if authentication successful
            
        Raises:
            AuthenticationError: If credentials are invalid
        """
        # Try to find user by username or email
        user = User.query.filter(
            (User.username == username.lower()) | (User.email == username.lower())
        ).first()
        
        if not user:
            raise AuthenticationError("Invalid username or password")
        
        # Check if account is active
        if not user.is_active:
            raise AuthenticationError("Account is inactive")
        
        # Verify password
        if not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid username or password")
        
        return user
    
    @staticmethod
    def change_password(user: User, old_password: str, new_password: str) -> User:
        """
        Change user password
        
        Args:
            user: User object
            old_password: Current password
            new_password: New password
            
        Returns:
            Updated User object
            
        Raises:
            AuthenticationError: If old password is incorrect
            DatabaseError: If database operation fails
        """
        # Verify old password
        if not verify_password(old_password, user.password_hash):
            raise AuthenticationError("Current password is incorrect")
        
        try:
            # Hash new password
            user.password_hash = hash_password(new_password)
            db.session.commit()
            
            return user
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(f"Failed to update password: {str(e)}")
