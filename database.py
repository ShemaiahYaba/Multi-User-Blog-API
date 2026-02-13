"""
Database configuration and initialization

Handles SQLAlchemy setup and Flask-Migrate integration.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    """
    Initialize database with Flask app
    
    Args:
        app: Flask application instance
    """
    # Initialize SQLAlchemy with app
    db.init_app(app)
    
    # Initialize Flask-Migrate with app and db
    migrate.init_app(app, db)
    
    # Create tables if they don't exist (for SQLite development)
    with app.app_context():
        db.create_all()
