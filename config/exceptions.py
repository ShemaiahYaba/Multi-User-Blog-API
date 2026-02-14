"""
Custom exceptions for the Blog API

Provides clear error types for different failure scenarios.
"""


class BlogAPIError(Exception):
    """Base exception for all blog API errors"""
    pass


class ValidationError(BlogAPIError):
    """Raised when input validation fails"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


class AuthenticationError(BlogAPIError):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        self.message = message
        super().__init__(self.message)


class AuthorizationError(BlogAPIError):
    """Raised when user lacks permission"""
    def __init__(self, message: str = "You don't have permission to perform this action"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(BlogAPIError):
    """Raised when a user doesn't exist"""
    def __init__(self, user_id: int = None):
        self.user_id = user_id
        self.message = f"User with ID {user_id} not found" if user_id else "User not found"
        super().__init__(self.message)


class PostNotFoundError(BlogAPIError):
    """Raised when a post doesn't exist"""
    def __init__(self, post_id: int = None):
        self.post_id = post_id
        self.message = f"Post with ID {post_id} not found" if post_id else "Post not found"
        super().__init__(self.message)


class DuplicateUserError(BlogAPIError):
    """Raised when attempting to create duplicate user"""
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        self.message = f"User with {field} '{value}' already exists"
        super().__init__(self.message)


class InvalidTokenError(BlogAPIError):
    """Raised when JWT token is invalid"""
    def __init__(self, message: str = "Invalid or expired token"):
        self.message = message
        super().__init__(self.message)


class DatabaseError(BlogAPIError):
    """Raised when a database operation fails"""
    def __init__(self, message: str = "Database operation failed"):
        self.message = message
        super().__init__(self.message)
