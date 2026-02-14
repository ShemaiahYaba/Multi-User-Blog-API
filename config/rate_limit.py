"""
Rate Limiting Module

Provides rate limiting functionality for the API.
Can be enabled/disabled via RATE_LIMIT_ENABLED environment variable.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Global limiter instance
limiter = None


def init_limiter(app):
    """
    Initialize rate limiter for the Flask app
    
    Args:
        app: Flask application instance
        
    Returns:
        Limiter instance if enabled, None otherwise
    """
    global limiter
    
    if not app.config.get('RATELIMIT_ENABLED', False):
        print("ℹ️  Rate limiting: DISABLED")
        return None
    
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=app.config.get('RATELIMIT_STORAGE_URI'),
        storage_options={},
        strategy=app.config.get('RATELIMIT_STRATEGY'),
        default_limits=[app.config.get('RATELIMIT_DEFAULT')],
        headers_enabled=app.config.get('RATELIMIT_HEADERS_ENABLED', True)
    )
    
    print(f"✅ Rate limiting: ENABLED ({app.config.get('RATELIMIT_DEFAULT')})")
    
    return limiter


def get_limiter():
    """
    Get the global limiter instance
    
    Returns:
        Limiter instance or None if disabled
    """
    return limiter
