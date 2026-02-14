"""
Seed script - Populate database with sample data

Creates:
- 1 admin user
- 3 regular users
- 10 blog posts
"""

from pathlib import Path
import sys

# Allow direct execution (`python db/seed.py`) by exposing project root on sys.path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from db import db
from models import User, Post
from utils.security import hash_password


def seed_database():
    """Seed the database with sample data"""
    
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        Post.query.delete()
        User.query.delete()
        db.session.commit()
        
        print("Creating users...")
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@blog.com',
            password_hash=hash_password('Admin123!'),
            role='admin',
            is_active=True
        )
        
        # Create regular users
        john = User(
            username='john_doe',
            email='john@example.com',
            password_hash=hash_password('Password123!'),
            role='user',
            is_active=True
        )
        
        jane = User(
            username='jane_smith',
            email='jane@example.com',
            password_hash=hash_password('Password123!'),
            role='user',
            is_active=True
        )
        
        bob = User(
            username='bob_wilson',
            email='bob@example.com',
            password_hash=hash_password('Password123!'),
            role='user',
            is_active=True
        )
        
        db.session.add_all([admin, john, jane, bob])
        db.session.commit()
        
        print("Creating blog posts...")
        
        # John's posts
        post1 = Post(
            title="Getting Started with Flask",
            content="Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.",
            author_id=john.id
        )
        
        post2 = Post(
            title="Introduction to SQLAlchemy",
            content="SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. Learn how to use it effectively.",
            author_id=john.id
        )
        
        post3 = Post(
            title="REST API Best Practices",
            content="Building a REST API requires careful planning. Here are some best practices to follow when designing your API endpoints, handling errors, and managing authentication.",
            author_id=john.id
        )
        
        # Jane's posts
        post4 = Post(
            title="Understanding JWT Authentication",
            content="JSON Web Tokens (JWT) are an open standard for securely transmitting information between parties as a JSON object. This post explains how to implement JWT in your applications.",
            author_id=jane.id
        )
        
        post5 = Post(
            title="Python Security Best Practices",
            content="Security should be a top priority when building web applications. Learn about password hashing, SQL injection prevention, and other security measures.",
            author_id=jane.id
        )
        
        post6 = Post(
            title="Database Design Fundamentals",
            content="Good database design is crucial for application performance and scalability. This post covers normalization, indexing, and relationship design.",
            author_id=jane.id
        )
        
        post7 = Post(
            title="Testing Flask Applications",
            content="Testing is essential for maintaining code quality. Learn how to write unit tests and integration tests for your Flask applications using pytest.",
            author_id=jane.id
        )
        
        # Bob's posts
        post8 = Post(
            title="Deploying Flask to Production",
            content="Moving from development to production requires careful consideration. This guide covers deployment strategies, environment configuration, and monitoring.",
            author_id=bob.id
        )
        
        post9 = Post(
            title="API Documentation with OpenAPI",
            content="Good API documentation is essential for developers. Learn how to document your API using OpenAPI (Swagger) specification.",
            author_id=bob.id
        )
        
        post10 = Post(
            title="Microservices Architecture",
            content="Microservices offer benefits for large-scale applications. This post explores when to use microservices and how to design them effectively.",
            author_id=bob.id
        )
        
        db.session.add_all([post1, post2, post3, post4, post5, post6, post7, post8, post9, post10])
        db.session.commit()
        
        print("\n" + "="*70)
        print("✅ Database seeded successfully!")
        print("="*70)
        print(f"👥 Created {User.query.count()} users:")
        print(f"   • admin (admin@blog.com) - Admin role")
        print(f"   • john_doe (john@example.com) - User role")
        print(f"   • jane_smith (jane@example.com) - User role")
        print(f"   • bob_wilson (bob@example.com) - User role")
        print(f"\n📝 Created {Post.query.count()} blog posts:")
        print(f"   • John: {john.posts.count()} posts")
        print(f"   • Jane: {jane.posts.count()} posts")
        print(f"   • Bob: {bob.posts.count()} posts")
        print("\n🔑 Test credentials (all passwords: Password123!):")
        print("   • admin / Admin123!")
        print("   • john_doe / Password123!")
        print("   • jane_smith / Password123!")
        print("   • bob_wilson / Password123!")
        print("="*70 + "\n")


if __name__ == '__main__':
    print("\n🌱 Seeding database with sample data...\n")
    seed_database()
