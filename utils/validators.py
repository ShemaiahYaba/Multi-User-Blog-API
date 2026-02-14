"""
Validation utilities - Helper functions for input validation
"""

from config import ValidationError


def validate_pagination(page: int = None, per_page: int = None) -> tuple:
    """
    Validate and normalize pagination parameters
    
    Args:
        page: Page number (1-indexed)
        per_page: Items per page
        
    Returns:
        Tuple of (page, per_page) with validated values
        
    Raises:
        ValidationError: If parameters are invalid
    """
    # Default values
    page = page if page is not None else 1
    per_page = per_page if per_page is not None else 10
    
    # Validate page
    try:
        page = int(page)
        if page < 1:
            raise ValidationError("Page must be >= 1", field="page")
    except (ValueError, TypeError):
        raise ValidationError("Page must be a number", field="page")
    
    # Validate per_page
    try:
        per_page = int(per_page)
        if per_page < 1:
            raise ValidationError("Per page must be >= 1", field="per_page")
        if per_page > 100:
            raise ValidationError("Per page must be <= 100", field="per_page")
    except (ValueError, TypeError):
        raise ValidationError("Per page must be a number", field="per_page")
    
    return page, per_page
