"""
Unit tests for security utilities

Tests password hashing and verification.
"""

import pytest
from utils.security import hash_password, verify_password


class TestPasswordHashing:
    """Test password hashing functions"""
    
    def test_hash_password(self, app):
        """Test password is hashed"""
        with app.app_context():
            password = "TestPassword123!"
            hashed = hash_password(password)
            
            # Hash should not equal original password
            assert hashed != password
            # Hash should be a string
            assert isinstance(hashed, str)
            # Hash should start with bcrypt identifier
            assert hashed.startswith('$2b$')
    
    def test_verify_password_correct(self, app):
        """Test correct password verification"""
        with app.app_context():
            password = "TestPassword123!"
            hashed = hash_password(password)
            
            # Correct password should verify
            assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self, app):
        """Test incorrect password verification"""
        with app.app_context():
            password = "TestPassword123!"
            wrong_password = "WrongPassword123!"
            hashed = hash_password(password)
            
            # Incorrect password should not verify
            assert verify_password(wrong_password, hashed) is False
    
    def test_same_password_different_hashes(self, app):
        """Test same password produces different hashes (salt)"""
        with app.app_context():
            password = "TestPassword123!"
            hash1 = hash_password(password)
            hash2 = hash_password(password)
            
            # Hashes should be different (different salts)
            assert hash1 != hash2
            # But both should verify
            assert verify_password(password, hash1) is True
            assert verify_password(password, hash2) is True
