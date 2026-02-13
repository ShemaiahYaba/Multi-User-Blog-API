"""
Common schemas - Reusable Pydantic models

Provides standard response formats used across the API.
"""

from typing import Generic, TypeVar, List, Any
from pydantic import BaseModel


# Generic type for paginated data
T = TypeVar('T')


class MessageResponse(BaseModel):
    """Standard message response"""
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed successfully"
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated response
    
    Used for any endpoint that returns paginated data.
    """
    items: List[T]
    total: int
    page: int
    per_page: int
    pages: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "per_page": 10,
                "pages": 10
            }
        }
