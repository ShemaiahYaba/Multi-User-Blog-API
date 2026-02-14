"""
Post model - Represents blog posts

Features:
- Database-level constraints
- Foreign key to User with cascade delete
- Indexes for performance
"""

from db import db
from .mixins import TimestampMixin


class Post(db.Model, TimestampMixin):
    """
    Post model representing blog posts
    
    Each post belongs to a user (author).
    When a user is deleted, their posts are also deleted (cascade).
    """
    __tablename__ = 'posts'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Post content with constraints
    title = db.Column(
        db.String(200),
        nullable=False,
        index=True
    )
    
    content = db.Column(
        db.Text,
        nullable=False
    )
    
    # Foreign key to User (author)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Database-level constraints
    __table_args__ = (
        # Ensure title is not empty
        db.CheckConstraint('length(title) > 0', name='title_not_empty'),
        # Ensure content has minimum length
        db.CheckConstraint('length(content) >= 10', name='content_min_length'),
        # Composite index for common queries
        db.Index('idx_post_author_created', 'author_id', 'created_at'),
    )
    
    def __repr__(self):
        return f'<Post {self.title[:30]}...>'
    
    def is_author(self, user_id: int) -> bool:
        """Check if given user is the author of this post"""
        return self.author_id == user_id
