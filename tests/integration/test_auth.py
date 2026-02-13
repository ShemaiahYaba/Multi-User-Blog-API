"""
Integration tests for authentication endpoints

Tests:
- User registration
- User login
- Token refresh
- Password validation
- Duplicate user prevention
"""

import pytest


class TestRegistration:
    """Test user registration endpoint"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post('/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'NewPassword123!'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert 'access_token' in data['data']
        assert 'refresh_token' in data['data']
        assert data['data']['user']['username'] == 'newuser'
        assert data['data']['user']['role'] == 'user'
    
    def test_register_duplicate_username(self, client, sample_user):
        """Test registration with duplicate username"""
        response = client.post('/auth/register', json={
            'username': 'testuser',  # Already exists
            'email': 'different@example.com',
            'password': 'NewPassword123!'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'testuser' in data['error'].lower()
    
    def test_register_duplicate_email(self, client, sample_user):
        """Test registration with duplicate email"""
        response = client.post('/auth/register', json={
            'username': 'differentuser',
            'email': 'test@example.com',  # Already exists
            'password': 'NewPassword123!'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'email' in data['error'].lower()
    
    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post('/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'weak'  # Too weak
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        response = client.post('/auth/register', json={
            'username': 'newuser',
            'email': 'notanemail',
            'password': 'StrongPass123!'
        })
        
        assert response.status_code == 400
    
    def test_register_missing_fields(self, client):
        """Test registration with missing required fields"""
        response = client.post('/auth/register', json={
            'username': 'newuser'
            # Missing email and password
        })
        
        assert response.status_code == 400


class TestLogin:
    """Test user login endpoint"""
    
    def test_login_success(self, client, sample_user):
        """Test successful login"""
        response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'access_token' in data['data']
        assert 'refresh_token' in data['data']
        assert data['data']['user']['username'] == 'testuser'
    
    def test_login_with_email(self, client, sample_user):
        """Test login using email instead of username"""
        response = client.post('/auth/login', json={
            'username': 'test@example.com',  # Email
            'password': 'TestPass123!'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_login_wrong_password(self, client, sample_user):
        """Test login with incorrect password"""
        response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'WrongPassword123!'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post('/auth/login', json={
            'username': 'nonexistent',
            'password': 'SomePassword123!'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False


class TestTokenRefresh:
    """Test token refresh endpoint"""
    
    def test_refresh_token_success(self, client, sample_user):
        """Test successful token refresh"""
        # Login to get refresh token
        login_response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        refresh_token = login_response.get_json()['data']['refresh_token']
        
        # Use refresh token to get new access token
        response = client.post('/auth/refresh',
            headers={'Authorization': f'Bearer {refresh_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'access_token' in data['data']
    
    def test_refresh_with_access_token_fails(self, client, user_token):
        """Test refresh with access token (should fail)"""
        response = client.post('/auth/refresh',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        
        assert response.status_code == 401
    
    def test_refresh_without_token(self, client):
        """Test refresh without token"""
        response = client.post('/auth/refresh')
        
        assert response.status_code == 401
