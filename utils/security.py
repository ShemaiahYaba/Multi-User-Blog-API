"""
Security utilities - Password hashing and verification

Uses bcrypt for secure password hashing.
NEVER store plain text passwords!
"""

import bcrypt
from flask import current_app


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password as string
        
    Example:
        >>> hashed = hash_password("MyPassword123!")
        >>> print(hashed)
        $2b$12$...
    """
    # Get bcrypt rounds from config (default: 12)
    rounds = current_app.config.get('BCRYPT_LOG_ROUNDS', 12)
    
    # Hash password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        password: Plain text password to verify
        password_hash: Stored hash to check against
        
    Returns:
        True if password matches, False otherwise
        
    Example:
        >>> hashed = hash_password("MyPassword123!")
        >>> verify_password("MyPassword123!", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False
    """
    password_bytes = password.encode('utf-8')
    hash_bytes = password_hash.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hash_bytes)
