"""
User model - Represents authenticated users

Features:
- Database-level constraints (unique, not null, check constraints)
- Password hashing (never stores plain text)
- Role-based access control
- Relationships with posts
"""

from db import db
from .mixins import TimestampMixin


class User(db.Model, TimestampMixin):
    """
    User model with authentication and authorization
    
    Roles:
    - 'user': Regular user (can CRUD own posts)
    - 'admin': Administrator (can delete any post)
    """
    __tablename__ = 'users'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # User credentials with database constraints
    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )
    
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )
    
    # Password hash (never store plain passwords!)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Role for authorization
    role = db.Column(
        db.String(20),
        nullable=False,
        default='user',
        index=True
    )
    
    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    posts = db.relationship(
        'Post',
        backref='author',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    # Database-level constraints
    __table_args__ = (
        # Ensure username is at least 3 characters
        db.CheckConstraint('length(username) >= 3', name='username_min_length'),
        # Ensure email contains @
        db.CheckConstraint("email LIKE '%@%'", name='email_format'),
        # Ensure role is valid
        db.CheckConstraint(
            "role IN ('user', 'admin')",
            name='valid_role'
        ),
        # Composite index for common queries
        db.Index('idx_user_active_role', 'is_active', 'role'),
    )
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'admin'
