"""
Post service - Handles blog post operations

Business logic for:
- Creating posts
- Reading posts
- Updating posts (with ownership check)
- Deleting posts (with ownership/admin check)
"""

from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import Post, User
from utils.validators import validate_pagination
from config import (
    PostNotFoundError,
    AuthorizationError,
    DatabaseError,
    ValidationError
)


class PostService:
    """Service for post operations"""
    
    @staticmethod
    def get_all_posts(page: int = 1, per_page: int = 10) -> dict:
        """
        Get all posts with pagination
        
        Args:
            page: Page number (1-indexed)
            per_page: Items per page
            
        Returns:
            Dictionary with posts and pagination info
            
        Raises:
            ValidationError: If pagination parameters are invalid
            DatabaseError: If database operation fails
        """
        # Validate pagination
        page, per_page = validate_pagination(page, per_page)
        
        try:
            # Query posts ordered by creation date (newest first)
            paginated = Post.query.order_by(
                Post.created_at.desc()
            ).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            return {
                'items': paginated.items,
                'total': paginated.total,
                'page': page,
                'per_page': per_page,
                'pages': paginated.pages
            }
            
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to fetch posts: {str(e)}")
    
    @staticmethod
    def get_post_by_id(post_id: int) -> Post:
        """
        Get post by ID
        
        Args:
            post_id: Post ID
            
        Returns:
            Post object
            
        Raises:
            PostNotFoundError: If post doesn't exist
        """
        post = db.session.get(Post, post_id)
        if not post:
            raise PostNotFoundError(post_id)
        return post
    
    @staticmethod
    def get_posts_by_user(user_id: int, page: int = 1, per_page: int = 10) -> dict:
        """
        Get posts by specific user with pagination
        
        Args:
            user_id: User ID
            page: Page number
            per_page: Items per page
            
        Returns:
            Dictionary with posts and pagination info
            
        Raises:
            ValidationError: If pagination parameters are invalid
            DatabaseError: If database operation fails
        """
        # Validate pagination
        page, per_page = validate_pagination(page, per_page)
        
        try:
            paginated = Post.query.filter_by(
                author_id=user_id
            ).order_by(
                Post.created_at.desc()
            ).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            return {
                'items': paginated.items,
                'total': paginated.total,
                'page': page,
                'per_page': per_page,
                'pages': paginated.pages
            }
            
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to fetch user posts: {str(e)}")
    
    @staticmethod
    def create_post(title: str, content: str, author_id: int) -> Post:
        """
        Create a new post
        
        Args:
            title: Post title
            content: Post content
            author_id: ID of the author (current user)
            
        Returns:
            Created Post object
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            post = Post(
                title=title,
                content=content,
                author_id=author_id
            )
            
            db.session.add(post)
            db.session.commit()
            
            return post
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(f"Failed to create post: {str(e)}")
    
    @staticmethod
    def update_post(post_id: int, user_id: int, title: str = None, content: str = None) -> Post:
        """
        Update a post
        
        Only the author can update their own post.
        
        Args:
            post_id: Post ID
            user_id: ID of the user attempting to update
            title: New title (optional)
            content: New content (optional)
            
        Returns:
            Updated Post object
            
        Raises:
            PostNotFoundError: If post doesn't exist
            AuthorizationError: If user is not the author
            DatabaseError: If database operation fails
        """
        post = PostService.get_post_by_id(post_id)
        
        # Check ownership
        if not post.is_author(user_id):
            raise AuthorizationError("You can only update your own posts")
        
        try:
            # Update fields if provided
            if title is not None:
                post.title = title
            if content is not None:
                post.content = content
            
            db.session.commit()
            return post
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(f"Failed to update post: {str(e)}")
    
    @staticmethod
    def delete_post(post_id: int, user_id: int, user_role: str) -> Post:
        """
        Delete a post
        
        Authors can delete their own posts.
        Admins can delete any post.
        
        Args:
            post_id: Post ID
            user_id: ID of the user attempting to delete
            user_role: Role of the user ('user' or 'admin')
            
        Returns:
            Deleted Post object
            
        Raises:
            PostNotFoundError: If post doesn't exist
            AuthorizationError: If user lacks permission
            DatabaseError: If database operation fails
        """
        post = PostService.get_post_by_id(post_id)
        
        # Check authorization
        # Admin can delete any post, or user can delete their own post
        if user_role != 'admin' and not post.is_author(user_id):
            raise AuthorizationError("You can only delete your own posts")
        
        try:
            db.session.delete(post)
            db.session.commit()
            return post
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(f"Failed to delete post: {str(e)}")
