"""
Post routes - Blog post management

Public endpoints:
- GET /posts - List all posts (paginated)
- GET /posts/:id - Get specific post

Protected endpoints (authentication required):
- POST /posts - Create new post
- PUT /posts/:id - Update own post
- DELETE /posts/:id - Delete own post (or any post if admin)
"""

from flask import Blueprint, request
from pydantic import ValidationError as PydanticValidationError

from services import PostService
from schemas import PostCreate, PostUpdate, PostResponse, PostBrief, PaginatedResponse
from utils import create_success_response, create_error_response
from middleware import jwt_required, get_current_user
from config import (
    PostNotFoundError,
    AuthenticationError,
    AuthorizationError,
    DatabaseError,
    ValidationError
)

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')


# ==================== PUBLIC ENDPOINTS ====================

@posts_bp.route('', methods=['GET'])
def get_posts():
    """
    Get all posts with pagination (PUBLIC)
    
    Query parameters:
        page: Page number (default: 1)
        per_page: Items per page (default: 10, max: 100)
    
    Returns:
        200: Paginated list of posts
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = PostService.get_all_posts(page=page, per_page=per_page)
        
        # Convert posts to brief schema
        posts_brief = [PostBrief.model_validate(post) for post in result['items']]
        
        return create_success_response(
            data={
                'items': [p.model_dump() for p in posts_brief],
                'total': result['total'],
                'page': result['page'],
                'per_page': result['per_page'],
                'pages': result['pages']
            }
        )
        
    except ValidationError as e:
        return create_error_response(str(e), 400)
    except DatabaseError as e:
        return create_error_response(str(e), 500)


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Get specific post by ID (PUBLIC)
    
    Returns:
        200: Post details
        404: Post not found
    """
    try:
        post = PostService.get_post_by_id(post_id)
        return create_success_response(
            data=PostResponse.model_validate(post)
        )
        
    except PostNotFoundError as e:
        return create_error_response(str(e), 404)
    except DatabaseError as e:
        return create_error_response(str(e), 500)


# ==================== PROTECTED ENDPOINTS ====================

@posts_bp.route('', methods=['POST'])
@jwt_required
def create_post():
    """
    Create new post (AUTHENTICATED)
    
    Headers:
        Authorization: Bearer <access_token>
    
    Request body:
        {
            "title": "My Blog Post",
            "content": "Post content goes here..."
        }
    
    Returns:
        201: Post created
        400: Validation error
        401: Unauthorized
    """
    if not request.is_json:
        return create_error_response("Content-Type must be application/json", 400)
    
    try:
        user = get_current_user()
        
        # Validate request
        schema = PostCreate(**request.get_json())
        
        # Create post
        post = PostService.create_post(
            title=schema.title,
            content=schema.content,
            author_id=user.id
        )
        
        return create_success_response(
            data=PostResponse.model_validate(post),
            message="Post created successfully",
            status_code=201
        )
        
    except PydanticValidationError as e:
        errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        return create_error_response("; ".join(errors), 400)
    except AuthenticationError as e:
        return create_error_response(str(e), 401)
    except DatabaseError as e:
        return create_error_response(str(e), 500)


@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required
def update_post(post_id):
    """
    Update post (AUTHENTICATED - own posts only)
    
    Headers:
        Authorization: Bearer <access_token>
    
    Request body (all optional):
        {
            "title": "Updated Title",
            "content": "Updated content..."
        }
    
    Returns:
        200: Post updated
        400: Validation error
        401: Unauthorized
        403: Forbidden (not post owner)
        404: Post not found
    """
    if not request.is_json:
        return create_error_response("Content-Type must be application/json", 400)
    
    try:
        user = get_current_user()
        
        # Validate request
        schema = PostUpdate(**request.get_json())
        
        # Update post
        post = PostService.update_post(
            post_id=post_id,
            user_id=user.id,
            title=schema.title,
            content=schema.content
        )
        
        return create_success_response(
            data=PostResponse.model_validate(post),
            message="Post updated successfully"
        )
        
    except PydanticValidationError as e:
        errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        return create_error_response("; ".join(errors), 400)
    except PostNotFoundError as e:
        return create_error_response(str(e), 404)
    except AuthenticationError as e:
        return create_error_response(str(e), 401)
    except AuthorizationError as e:
        return create_error_response(str(e), 403)
    except DatabaseError as e:
        return create_error_response(str(e), 500)


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required
def delete_post(post_id):
    """
    Delete post (AUTHENTICATED - own posts or admin)
    
    Regular users can only delete their own posts.
    Admins can delete any post.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: Post deleted
        401: Unauthorized
        403: Forbidden (not post owner)
        404: Post not found
    """
    try:
        user = get_current_user()
        
        # Delete post (checks ownership/admin in service)
        post = PostService.delete_post(
            post_id=post_id,
            user_id=user.id,
            user_role=user.role
        )
        
        return create_success_response(
            message=f'Post "{post.title}" deleted successfully'
        )
        
    except PostNotFoundError as e:
        return create_error_response(str(e), 404)
    except AuthenticationError as e:
        return create_error_response(str(e), 401)
    except AuthorizationError as e:
        return create_error_response(str(e), 403)
    except DatabaseError as e:
        return create_error_response(str(e), 500)
