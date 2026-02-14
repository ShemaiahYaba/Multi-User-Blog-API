"""
Swagger/OpenAPI Documentation Generator

Generates OpenAPI 3.0 specification for the Blog API.
Access documentation at /api/docs
"""

from apispec import APISpec
from flask import jsonify


def create_apispec():
    """Create APISpec instance with metadata"""
    return APISpec(
        title="Blog API with Authentication",
        version="1.0.0",
        openapi_version="3.0.0",
        info={
            "description": """
# Blog API Documentation

A production-ready RESTful blog API featuring:
- 🔐 JWT Authentication (access + refresh tokens)
- 👥 Role-Based Access Control (user, admin)
- 📝 Blog Post CRUD Operations
- ✅ Pydantic Schema Validation
- 🔒 Password Security (bcrypt)
- 🛡️ Ownership-based Authorization

## Authentication

Most endpoints require authentication. To authenticate:

1. **Register** or **Login** to get JWT tokens
2. Include the access token in the Authorization header:
   ```
   Authorization: Bearer <your_access_token>
   ```

## Roles

- **User**: Can create, read, update, and delete their own posts
- **Admin**: Can delete any post (in addition to user permissions)
            """,
            "contact": {
                "name": "API Support",
                "email": "support@blogapi.com"
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        servers=[
            {"url": "http://localhost:5000", "description": "Development server"},
            {"url": "http://localhost:5001", "description": "Alternative development server"}
        ],
    )


def get_apispec_dict(app):
    """
    Generate complete OpenAPI specification dictionary
    
    Args:
        app: Flask application instance
        
    Returns:
        OpenAPI specification as dictionary
    """
    spec = create_apispec()
    
    # Security schemes
    spec.components.security_scheme(
        "BearerAuth",
        {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT access token"
        }
    )
    
    # Define schemas
    _add_schemas(spec)
    
    # Define paths
    _add_paths(spec)
    
    return spec.to_dict()


def _add_schemas(spec):
    """Add schema definitions to spec"""
    
    # User schemas
    spec.components.schema(
        "UserRegister",
        {
            "type": "object",
            "required": ["username", "email", "password"],
            "properties": {
                "username": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 50,
                    "example": "john_doe"
                },
                "email": {
                    "type": "string",
                    "format": "email",
                    "example": "john@example.com"
                },
                "password": {
                    "type": "string",
                    "minLength": 8,
                    "example": "SecurePass123!",
                    "description": "Must contain uppercase, lowercase, number, and special character"
                }
            }
        }
    )
    
    spec.components.schema(
        "UserLogin",
        {
            "type": "object",
            "required": ["username", "password"],
            "properties": {
                "username": {"type": "string", "example": "john_doe"},
                "password": {"type": "string", "example": "SecurePass123!"}
            }
        }
    )
    
    spec.components.schema(
        "UserResponse",
        {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "username": {"type": "string", "example": "john_doe"},
                "email": {"type": "string", "example": "john@example.com"},
                "role": {"type": "string", "enum": ["user", "admin"], "example": "user"},
                "is_active": {"type": "boolean", "example": True},
                "created_at": {"type": "string", "format": "date-time"}
            }
        }
    )
    
    spec.components.schema(
        "TokenResponse",
        {
            "type": "object",
            "properties": {
                "access_token": {"type": "string"},
                "refresh_token": {"type": "string"},
                "token_type": {"type": "string", "example": "Bearer"},
                "expires_in": {"type": "integer", "example": 900},
                "user": {"$ref": "#/components/schemas/UserResponse"}
            }
        }
    )
    
    # Post schemas
    spec.components.schema(
        "PostCreate",
        {
            "type": "object",
            "required": ["title", "content"],
            "properties": {
                "title": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200,
                    "example": "My First Blog Post"
                },
                "content": {
                    "type": "string",
                    "minLength": 10,
                    "example": "This is the content of my blog post..."
                }
            }
        }
    )
    
    spec.components.schema(
        "PostResponse",
        {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "title": {"type": "string", "example": "My First Blog Post"},
                "content": {"type": "string", "example": "This is the content..."},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
                "author": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "username": {"type": "string"},
                        "role": {"type": "string"}
                    }
                }
            }
        }
    )
    
    # Common schemas
    spec.components.schema(
        "Error",
        {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": False},
                "error": {"type": "string", "example": "Error message"}
            }
        }
    )


def _add_paths(spec):
    """Add API paths to spec"""
    
    # Auth endpoints
    spec.path(
        path="/auth/register",
        operations={
            "post": {
                "tags": ["Authentication"],
                "summary": "Register a new user",
                "description": "Create a new user account and receive JWT tokens",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UserRegister"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "User created successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "message": {"type": "string"},
                                        "data": {"$ref": "#/components/schemas/TokenResponse"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Validation error or duplicate user",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    }
                }
            }
        }
    )
    
    spec.path(
        path="/auth/login",
        operations={
            "post": {
                "tags": ["Authentication"],
                "summary": "Login user",
                "description": "Authenticate and receive JWT tokens",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UserLogin"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Login successful",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "data": {"$ref": "#/components/schemas/TokenResponse"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {"description": "Invalid credentials"}
                }
            }
        }
    )
    
    spec.path(
        path="/auth/refresh",
        operations={
            "post": {
                "tags": ["Authentication"],
                "summary": "Refresh access token",
                "description": "Get a new access token using refresh token",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "New access token",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "access_token": {"type": "string"},
                                                "token_type": {"type": "string"},
                                                "expires_in": {"type": "integer"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "401": {"description": "Invalid or expired refresh token"}
                }
            }
        }
    )
    
    # User endpoints
    spec.path(
        path="/users/me",
        operations={
            "get": {
                "tags": ["Users"],
                "summary": "Get current user profile",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "User profile",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {"$ref": "#/components/schemas/UserResponse"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {"description": "Unauthorized"}
                }
            },
            "put": {
                "tags": ["Users"],
                "summary": "Update current user profile",
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "email": {"type": "string", "format": "email"},
                                    "password": {"type": "string", "minLength": 8}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Profile updated"},
                    "400": {"description": "Validation error"},
                    "401": {"description": "Unauthorized"}
                }
            }
        }
    )
    
    # Post endpoints
    spec.path(
        path="/posts",
        operations={
            "get": {
                "tags": ["Posts"],
                "summary": "List all posts (public)",
                "parameters": [
                    {
                        "name": "page",
                        "in": "query",
                        "schema": {"type": "integer", "default": 1}
                    },
                    {
                        "name": "per_page",
                        "in": "query",
                        "schema": {"type": "integer", "default": 10}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Paginated list of posts",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "items": {
                                                    "type": "array",
                                                    "items": {"$ref": "#/components/schemas/PostResponse"}
                                                },
                                                "total": {"type": "integer"},
                                                "page": {"type": "integer"},
                                                "per_page": {"type": "integer"},
                                                "pages": {"type": "integer"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "tags": ["Posts"],
                "summary": "Create a new post (authenticated)",
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/PostCreate"}
                        }
                    }
                },
                "responses": {
                    "201": {"description": "Post created"},
                    "400": {"description": "Validation error"},
                    "401": {"description": "Unauthorized"}
                }
            }
        }
    )
    
    spec.path(
        path="/posts/{post_id}",
        operations={
            "get": {
                "tags": ["Posts"],
                "summary": "Get specific post (public)",
                "parameters": [
                    {
                        "name": "post_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Post details",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {"$ref": "#/components/schemas/PostResponse"}
                                    }
                                }
                            }
                        }
                    },
                    "404": {"description": "Post not found"}
                }
            },
            "put": {
                "tags": ["Posts"],
                "summary": "Update post (owner only)",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "post_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "content": {"type": "string"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Post updated"},
                    "401": {"description": "Unauthorized"},
                    "403": {"description": "Forbidden (not owner)"},
                    "404": {"description": "Post not found"}
                }
            },
            "delete": {
                "tags": ["Posts"],
                "summary": "Delete post (owner or admin)",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "post_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {"description": "Post deleted"},
                    "401": {"description": "Unauthorized"},
                    "403": {"description": "Forbidden (not owner or admin)"},
                    "404": {"description": "Post not found"}
                }
            }
        }
    )


def setup_swagger(app):
    """
    Setup Swagger UI for the Flask app
    
    Args:
        app: Flask application instance
    """
    from flask_swagger_ui import get_swaggerui_blueprint
    
    # Swagger UI configuration
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/spec'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Blog API Documentation",
            'layout': "BaseLayout",
            'deepLinking': True,
            'displayRequestDuration': True,
            'docExpansion': 'list',
            'filter': True,
            'showExtensions': True,
            'showCommonExtensions': True
        }
    )
    
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # OpenAPI spec endpoint
    @app.route('/api/spec')
    def spec():
        return jsonify(get_apispec_dict(app))
    
    port = app.config.get('PORT', 5000)
    if not hasattr(app, '_swagger_printed'):
        print(f"Swagger UI: http://localhost:{port}{SWAGGER_URL}")
        app._swagger_printed = True
