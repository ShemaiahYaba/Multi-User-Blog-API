"""
Post schemas - Pydantic models for blog post operations

Provides validation and serialization for:
- Creating posts
- Updating posts
- Post responses with author info
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .user import UserBrief


class PostCreate(BaseModel):
    """
    Schema for creating a new post
    
    Validates:
    - Title length (1-200 characters)
    - Content length (min 10 characters)
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Post title"
    )
    content: str = Field(
        ...,
        min_length=10,
        description="Post content (minimum 10 characters)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "My First Blog Post",
                "content": "This is the content of my first blog post. It contains interesting information about web development and best practices."
            }
        }


class PostUpdate(BaseModel):
    """
    Schema for updating an existing post
    
    All fields are optional - only provided fields will be updated.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=10)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Blog Post Title",
                "content": "Updated content with new information."
            }
        }


class PostBrief(BaseModel):
    """Brief post info (for lists)"""
    id: int
    title: str
    created_at: datetime
    author: UserBrief
    
    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    """
    Schema for post response with full details
    
    Includes author information as nested object.
    """
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    author: UserBrief  # Nested user info
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "My First Blog Post",
                "content": "This is the full content...",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00",
                "author": {
                    "id": 1,
                    "username": "john_doe",
                    "role": "user"
                }
            }
        }
