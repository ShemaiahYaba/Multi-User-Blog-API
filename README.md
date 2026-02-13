# Blog API with Authentication - Week 4 Project

A production-ready RESTful blog API featuring user authentication, role-based access control, and comprehensive security measures.

## 🎯 Project Overview

This project demonstrates professional backend development with:

- ✅ **JWT Authentication** - Access and refresh tokens
- ✅ **Role-Based Access Control** - User and Admin roles
- ✅ **Pydantic Schema Validation** - Type-safe request/response
- ✅ **Database Constraints** - Data integrity at DB level
- ✅ **Password Security** - Bcrypt hashing, strength validation
- ✅ **Ownership Authorization** - Users can only edit their own posts
- ✅ **Comprehensive Testing** - 90%+ code coverage
- ✅ **Clean Architecture** - Modular, testable, scalable

## 📁 Project Structure

```
blog-api/
├── app.py                      # Application factory
├── config.py                   # Configuration (dev, test, prod)
├── database.py                 # SQLAlchemy setup
├── exceptions.py               # Custom exceptions
│
├── models/                     # Database models
│   ├── __init__.py
│   ├── user.py                # User model with constraints
│   ├── post.py                # Post model with constraints
│   └── mixins.py              # Reusable model components
│
├── schemas/                    # Pydantic validation
│   ├── __init__.py
│   ├── user.py                # UserRegister, UserResponse, etc.
│   ├── post.py                # PostCreate, PostResponse, etc.
│   ├── auth.py                # TokenResponse, RefreshToken
│   └── common.py              # Pagination, Message schemas
│
├── services/                   # Business logic
│   ├── __init__.py
│   ├── auth_service.py        # Registration, login
│   ├── user_service.py        # User management
│   └── post_service.py        # Post CRUD with authorization
│
├── middleware/                 # Custom middleware
│   ├── __init__.py
│   └── auth.py                # JWT decorators
│
├── routes/                     # API endpoints
│   ├── __init__.py
│   ├── auth_routes.py         # /auth/*
│   ├── user_routes.py         # /users/*
│   ├── post_routes.py         # /posts/*
│   └── info_routes.py         # / and /health
│
├── utils/                      # Utilities
│   ├── __init__.py
│   ├── responses.py           # Response helpers
│   ├── security.py            # Password hashing
│   └── validators.py          # Input validation
│
├── tests/                      # Automated tests
│   ├── conftest.py            # Pytest fixtures
│   ├── unit/
│   │   └── test_security.py  # Unit tests
│   └── integration/
│       ├── test_auth.py       # Auth endpoint tests
│       └── test_posts.py      # Post endpoint tests
│
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── pytest.ini                  # Pytest configuration
├── seed.py                     # Sample data
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and set JWT_SECRET_KEY
```

### 2. Initialize Database

```bash
# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade

# Seed database (optional)
python seed.py
```

### 3. Run Application

```bash
python app.py
```

Server starts at: `http://localhost:5000`

### 4. Run Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests with coverage
pytest

# Run specific test file
pytest tests/integration/test_auth.py

# Run with markers
pytest -m unit        # Only unit tests
pytest -m integration # Only integration tests
```

## 📡 API Endpoints

### Authentication (`/auth`)

#### Register
```bash
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}

Response (201):
{
  "success": true,
  "data": {
    "access_token": "eyJ0eXAi...",
    "refresh_token": "eyJ0eXAi...",
    "token_type": "Bearer",
    "expires_in": 900,
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "role": "user",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00"
    }
  }
}
```

#### Login
```bash
POST /auth/login
Content-Type: application/json

{
  "username": "john_doe",  # or email
  "password": "SecurePass123!"
}

Response (200): Same as register
```

#### Refresh Token
```bash
POST /auth/refresh
Authorization: Bearer <refresh_token>

Response (200):
{
  "success": true,
  "data": {
    "access_token": "eyJ0eXAi...",
    "token_type": "Bearer",
    "expires_in": 900
  }
}
```

### Users (`/users`)

#### Get Profile
```bash
GET /users/me
Authorization: Bearer <access_token>

Response (200):
{
  "success": true,
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

#### Update Profile
```bash
PUT /users/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "email": "newemail@example.com",
  "password": "NewSecurePass123!"
}
```

### Posts (`/posts`)

#### List Posts (Public)
```bash
GET /posts?page=1&per_page=10

Response (200):
{
  "success": true,
  "data": {
    "items": [...],
    "total": 50,
    "page": 1,
    "per_page": 10,
    "pages": 5
  }
}
```

#### Get Post (Public)
```bash
GET /posts/1

Response (200):
{
  "success": true,
  "data": {
    "id": 1,
    "title": "My Blog Post",
    "content": "Post content...",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "author": {
      "id": 1,
      "username": "john_doe",
      "role": "user"
    }
  }
}
```

#### Create Post (Authenticated)
```bash
POST /posts
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "My First Post",
  "content": "This is my first blog post content."
}

Response (201): Full post object
```

#### Update Post (Owner Only)
```bash
PUT /posts/1
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content"
}

Response (200): Full post object
Response (403): If not owner
```

#### Delete Post (Owner or Admin)
```bash
DELETE /posts/1
Authorization: Bearer <access_token>

Response (200): Success message
Response (403): If not owner (unless admin)
```

## 🔐 Security Features

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character

### JWT Tokens
- **Access Token**: Short-lived (15 minutes)
- **Refresh Token**: Long-lived (7 days)
- Tokens include user ID as identity
- Automatic expiration handling

### Database Constraints
```sql
-- Username constraints
CHECK (length(username) >= 3)
UNIQUE (username)
INDEX (username)

-- Email constraints
CHECK (email LIKE '%@%')
UNIQUE (email)
INDEX (email)

-- Role constraints
CHECK (role IN ('user', 'admin'))
```

### Authorization Rules

| Action | User | Admin |
|--------|------|-------|
| View posts | ✅ Public | ✅ Public |
| Create post | ✅ Auth required | ✅ Auth required |
| Update own post | ✅ Yes | ✅ Yes |
| Update other's post | ❌ No | ❌ No |
| Delete own post | ✅ Yes | ✅ Yes |
| Delete any post | ❌ No | ✅ Yes |

## 🧪 Testing

### Test Coverage
- Unit tests: Security, validation, business logic
- Integration tests: Full request/response cycles
- Target coverage: 90%+

### Run Tests
```bash
# All tests with coverage
pytest --cov

# Specific test categories
pytest -m unit
pytest -m integration
pytest -m auth
pytest -m security

# Generate HTML coverage report
pytest --cov --cov-report=html
open htmlcov/index.html
```

### Sample Test Data
After running `python seed.py`:

```
Users:
- admin / Admin123! (admin role)
- john_doe / Password123! (user role)
- jane_smith / Password123! (user role)
- bob_wilson / Password123! (user role)

Posts:
- 10 blog posts across all users
```

## 🎓 Week 4 Learning Objectives

### ✅ Completed

**Authentication:**
- [x] User registration with validation
- [x] Login with JWT token generation
- [x] Token refresh mechanism
- [x] Password hashing (bcrypt)

**Authorization:**
- [x] Protected routes with decorators
- [x] Ownership-based permissions
- [x] Role-based access control (RBAC)
- [x] Admin override permissions

**Security:**
- [x] Password strength validation
- [x] SQL injection prevention (SQLAlchemy)
- [x] Input sanitization (Pydantic)
- [x] CORS configuration
- [x] Environment variables for secrets
- [x] Database-level constraints

**Architecture:**
- [x] Pydantic schema layer (Week 3 feedback)
- [x] Database constraints (Week 3 feedback)
- [x] Automated tests 90%+ (Week 3 feedback)

## 🚦 Next Steps

### Week 5 Preview - Deployment
- Containerization with Docker
- Environment configuration
- Production database setup
- CI/CD pipeline
- Monitoring and logging

### Potential Enhancements
- [ ] Email verification
- [ ] Password reset flow
- [ ] Rate limiting
- [ ] API documentation (Swagger/OpenAPI)
- [ ] File uploads (profile pictures, images)
- [ ] Post comments
- [ ] Post likes/reactions
- [ ] User follow system
- [ ] Search functionality

## 📝 Environment Variables

```bash
# Flask
FLASK_ENV=development
DEBUG=True
PORT=5000

# Database
DATABASE_URL=sqlite:///blog.db

# JWT
JWT_SECRET_KEY=your-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=900
JWT_REFRESH_TOKEN_EXPIRES=604800

# Security
BCRYPT_LOG_ROUNDS=12

# CORS
CORS_ORIGINS=http://localhost:3000
```

## 🐛 Common Issues

### Issue: Module not found
```bash
pip install -r requirements.txt
```

### Issue: Database locked (SQLite)
```bash
# Delete database and recreate
rm blog.db
flask db upgrade
python seed.py
```

### Issue: JWT decode error
```bash
# Set JWT_SECRET_KEY in .env
JWT_SECRET_KEY=a-very-secret-key-change-this
```

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Pydantic](https://docs.pydantic.dev/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pytest](https://docs.pytest.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## 🎉 Summary

This Week 4 project demonstrates:
- Production-ready authentication system
- Clean, testable architecture
- Security best practices
- Comprehensive testing
- All improvements from Week 3 feedback

**Total Files Created**: 38
**Lines of Code**: ~3000+
**Test Coverage**: 90%+
**Security Features**: 10+
**Architecture Layers**: 7

Ready for Week 5: Deployment! 🚀
