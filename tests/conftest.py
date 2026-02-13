"""
Pytest fixtures - Shared test utilities

Provides fixtures for:
- Flask app with test configuration
- Database setup/teardown
- Test client
- Sample users and tokens
"""

import pytest
from app import create_app
from database import db
from models import User, Post
from utils.security import hash_password


@pytest.fixture(scope='function')
def app():
    """Create Flask app with test configuration"""
    import os
    os.environ['FLASK_ENV'] = 'testing'
    
    app = create_app()
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Create CLI test runner"""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def sample_user(app):
    """Create a sample user"""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash=hash_password('TestPass123!'),
            role='user',
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


@pytest.fixture(scope='function')
def sample_admin(app):
    """Create a sample admin user"""
    with app.app_context():
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=hash_password('AdminPass123!'),
            role='admin',
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        db.session.refresh(admin)
        return admin


@pytest.fixture(scope='function')
def user_token(client, sample_user):
    """Get JWT token for regular user"""
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'TestPass123!'
    })
    data = response.get_json()
    return data['data']['access_token']


@pytest.fixture(scope='function')
def admin_token(client, sample_admin):
    """Get JWT token for admin user"""
    response = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'AdminPass123!'
    })
    data = response.get_json()
    return data['data']['access_token']


@pytest.fixture(scope='function')
def sample_post(app, sample_user):
    """Create a sample post"""
    with app.app_context():
        post = Post(
            title='Test Post',
            content='This is a test post content with enough characters.',
            author_id=sample_user.id
        )
        db.session.add(post)
        db.session.commit()
        db.session.refresh(post)
        return post


@pytest.fixture(scope='function')
def auth_headers(user_token):
    """Get authorization headers with user token"""
    return {'Authorization': f'Bearer {user_token}'}


@pytest.fixture(scope='function')
def admin_headers(admin_token):
    """Get authorization headers with admin token"""
    return {'Authorization': f'Bearer {admin_token}'}
