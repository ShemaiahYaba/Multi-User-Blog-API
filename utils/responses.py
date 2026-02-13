"""
Response utilities - Helper functions for API responses

Provides standardized success and error response formats.
"""

from flask import jsonify
from typing import Any, Optional


def create_success_response(
    data: Any = None,
    message: Optional[str] = None,
    status_code: int = 200
):
    """
    Create standardized success response
    
    Args:
        data: Response data (dict, list, or Pydantic model)
        message: Optional success message
        status_code: HTTP status code (default: 200)
        
    Returns:
        Tuple of (JSON response, status code)
    """
    response = {'success': True}
    
    if message:
        response['message'] = message
    
    if data is not None:
        # If data is a Pydantic model, convert to dict
        if hasattr(data, 'model_dump'):
            response['data'] = data.model_dump()
        else:
            response['data'] = data
    
    return jsonify(response), status_code


def create_error_response(
    error: Any,
    status_code: int = 400
):
    """
    Create standardized error response
    
    Args:
        error: Error message (string or exception)
        status_code: HTTP status code (default: 400)
        
    Returns:
        Tuple of (JSON response, status code)
    """
    return jsonify({
        'success': False,
        'error': str(error)
    }), status_code
