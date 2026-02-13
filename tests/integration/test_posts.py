"""
Integration tests for post endpoints

Tests:
- Public post viewing
- Creating posts (auth required)
- Updating own posts
- Deleting own posts
- Admin deleting any post
- Authorization checks
"""

import pytest


class TestPublicPostEndpoints:
    """Test public post endpoints (no auth required)"""
    
    def test_get_all_posts_empty(self, client):
        """Test getting posts when none exist"""
        response = client.get('/posts')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['total'] == 0
        assert data['data']['items'] == []
    
    def test_get_all_posts_with_data(self, client, sample_post):
        """Test getting posts when they exist"""
        response = client.get('/posts')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['total'] == 1
        assert len(data['data']['items']) == 1
    
    def test_get_single_post(self, client, sample_post):
        """Test getting specific post"""
        response = client.get(f'/posts/{sample_post.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['title'] == 'Test Post'
    
    def test_get_nonexistent_post(self, client):
        """Test getting non-existent post"""
        response = client.get('/posts/999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False


class TestProtectedPostEndpoints:
    """Test protected post endpoints (auth required)"""
    
    def test_create_post_success(self, client, auth_headers):
        """Test creating post with authentication"""
        response = client.post('/posts',
            headers=auth_headers,
            json={
                'title': 'New Post',
                'content': 'This is new post content with enough characters.'
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['title'] == 'New Post'
    
    def test_create_post_without_auth(self, client):
        """Test creating post without authentication"""
        response = client.post('/posts', json={
            'title': 'New Post',
            'content': 'This is new post content.'
        })
        
        assert response.status_code == 401
    
    def test_create_post_invalid_data(self, client, auth_headers):
        """Test creating post with invalid data"""
        response = client.post('/posts',
            headers=auth_headers,
            json={
                'title': 'Short',
                'content': 'Too short'  # Less than 10 chars
            }
        )
        
        assert response.status_code == 400
    
    def test_update_own_post(self, client, sample_post, auth_headers):
        """Test updating own post"""
        response = client.put(f'/posts/{sample_post.id}',
            headers=auth_headers,
            json={
                'title': 'Updated Title'
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['title'] == 'Updated Title'
    
    def test_update_other_user_post(self, client, sample_post):
        """Test updating another user's post (should fail)"""
        # Create different user and get their token
        client.post('/auth/register', json={
            'username': 'otheruser',
            'email': 'other@example.com',
            'password': 'OtherPass123!'
        })
        
        login_response = client.post('/auth/login', json={
            'username': 'otheruser',
            'password': 'OtherPass123!'
        })
        other_token = login_response.get_json()['data']['access_token']
        
        # Try to update original user's post
        response = client.put(f'/posts/{sample_post.id}',
            headers={'Authorization': f'Bearer {other_token}'},
            json={'title': 'Hacked Title'}
        )
        
        assert response.status_code == 403
        data = response.get_json()
        assert data['success'] is False
    
    def test_delete_own_post(self, client, sample_post, auth_headers):
        """Test deleting own post"""
        response = client.delete(f'/posts/{sample_post.id}',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_delete_other_user_post_as_user(self, client, sample_post):
        """Test deleting another user's post as regular user (should fail)"""
        # Create different user
        client.post('/auth/register', json={
            'username': 'otheruser',
            'email': 'other@example.com',
            'password': 'OtherPass123!'
        })
        
        login_response = client.post('/auth/login', json={
            'username': 'otheruser',
            'password': 'OtherPass123!'
        })
        other_token = login_response.get_json()['data']['access_token']
        
        # Try to delete original user's post
        response = client.delete(f'/posts/{sample_post.id}',
            headers={'Authorization': f'Bearer {other_token}'}
        )
        
        assert response.status_code == 403


class TestAdminPermissions:
    """Test admin-specific permissions"""
    
    def test_admin_can_delete_any_post(self, client, sample_post, admin_headers):
        """Test admin can delete any user's post"""
        response = client.delete(f'/posts/{sample_post.id}',
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True


class TestPagination:
    """Test post pagination"""
    
    def test_pagination_default(self, client, app):
        """Test default pagination"""
        # Create multiple posts
        with app.app_context():
            from models import User, Post
            from database import db
            from utils.security import hash_password
            
            user = User(
                username='paginationuser',
                email='pagination@example.com',
                password_hash=hash_password('TestPass123!'),
                role='user'
            )
            db.session.add(user)
            db.session.commit()
            
            # Create 15 posts
            for i in range(15):
                post = Post(
                    title=f'Post {i}',
                    content=f'Content for post {i} with enough characters here.',
                    author_id=user.id
                )
                db.session.add(post)
            db.session.commit()
        
        response = client.get('/posts')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['data']['total'] == 15
        assert data['data']['per_page'] == 10
        assert len(data['data']['items']) == 10
    
    def test_pagination_custom(self, client, app):
        """Test custom pagination parameters"""
        response = client.get('/posts?page=2&per_page=5')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['data']['page'] == 2
        assert data['data']['per_page'] == 5
