"""
Database configuration and initialization

Handles SQLAlchemy setup and Flask-Migrate integration.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    """
    Initialize database with Flask app
    
    Args:
        app: Flask application instance
    """
    # Ensure SQLite parent directory exists before connecting.
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if db_uri.startswith("sqlite:///") and not db_uri.endswith(":memory:"):
        db_path = db_uri.replace("sqlite:///", "", 1).split("?", 1)[0]
        parent_dir = os.path.dirname(db_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

    # Initialize SQLAlchemy with app
    db.init_app(app)
    
    # Initialize Flask-Migrate with app and db
    migrate.init_app(app, db)
    
    # Create tables if they don't exist (for SQLite development)
    with app.app_context():
        db.create_all()
