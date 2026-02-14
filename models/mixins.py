"""
Model mixins - Reusable model components

Provides common functionality for SQLAlchemy models.
"""

from datetime import datetime
from db import db


class TimestampMixin:
    """
    Mixin to add created_at and updated_at timestamps to models
    
    Automatically sets:
    - created_at on insert
    - updated_at on insert and update
    """
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
