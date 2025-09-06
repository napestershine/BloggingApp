# FastAPI Blog API

A modern FastAPI-based blog API with JWT authentication, designed to replicate the functionality of the Symfony blog API.

## Features

- **JWT Authentication**: Secure user authentication and authorization
- **User Management**: User registration, login, and profile management
- **Blog Posts**: Create, read, update blog posts with author access control
- **Comments**: Add and manage comments on blog posts
- **Database Models**: SQLAlchemy models for User, BlogPost, and Comment entities
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token

### Users
- `GET /users/{user_id}` - Get user details (authenticated)
- `PUT /users/{user_id}` - Update user profile (own profile only)

### Blog Posts
- `GET /blog_posts/` - List all blog posts
- `POST /blog_posts/` - Create a new blog post (authenticated)
- `GET /blog_posts/{post_id}` - Get specific blog post
- `PUT /blog_posts/{post_id}` - Update blog post (author only)

### Comments
- `GET /comments/` - List all comments
- `POST /comments/` - Create a new comment (authenticated)
- `GET /comments/{comment_id}` - Get specific comment
- `PUT /comments/{comment_id}` - Update comment (author only)
- `GET /comments/blog_post/{blog_post_id}` - Get comments for a blog post

## Setup

### Docker Setup (Recommended)

1. Build and run with Docker Compose:
```bash
docker compose up --build
```

2. The API will be available at: http://localhost:8000
3. View API documentation at: http://localhost:8000/docs

### Manual Setup

1. Install Python 3.12+ and create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

5. Access the application:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## Database

### SQLite (Development)
The application uses SQLite by default for development. The database file will be created automatically.

### PostgreSQL (Production)
For production, update the `DATABASE_URL` in your `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost:5432/blog_db
```

## Usage Examples

### Register a User
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "name": "John Doe",
       "password": "SecurePass123",
       "retyped_password": "SecurePass123"
     }'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=SecurePass123"
```

### Create a Blog Post (with token)
```bash
curl -X POST "http://localhost:8000/blog_posts/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -d '{
       "title": "My First Post",
       "content": "This is the content of my first blog post.",
       "slug": "my-first-post"
     }'
```

### Create a Comment (with token)
```bash
curl -X POST "http://localhost:8000/comments/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -d '{
       "content": "Great post!",
       "blog_post_id": 1
     }'
```

## Development

### Running Tests

The application supports both SQLite and PostgreSQL for testing:

#### Local Development (SQLite)
```bash
pytest
```

#### CI/Production Testing (PostgreSQL)
```bash
# Set TEST_DATABASE_URL environment variable to use PostgreSQL
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/test_db pytest
```

#### GitHub Actions CI
Tests automatically run with PostgreSQL in CI environment. The GitHub Actions workflow:
- Starts a PostgreSQL 15 service
- Sets up the test database (blog_test)
- Runs all tests with PostgreSQL

#### Database-specific Testing
Run the database integration test to verify both SQLite and PostgreSQL compatibility:
```bash
# Test with SQLite (default)
pytest app/tests/test_database_integration.py -v

# Test with PostgreSQL (requires running PostgreSQL instance)
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/blog_test \
  pytest app/tests/test_database_integration.py -v
```

### Code Formatting
```bash
black app/
isort app/
```

### Type Checking
```bash
mypy app/
```

## Migration from Symfony

This FastAPI application replicates the core functionality of the original Symfony blog API:

- **User Model**: Matches Symfony User entity with username, email, name, and password
- **BlogPost Model**: Equivalent to Symfony BlogPost with title, content, slug, and author relationship
- **Comment Model**: Similar to Symfony Comment with content and relationships to user and blog post
- **Authentication**: JWT-based authentication similar to LexikJWTAuthenticationBundle
- **Access Control**: Route-level authorization matching Symfony's access control rules

## Security Notes

- Change the `SECRET_KEY` in production
- Use HTTPS in production
- Configure CORS appropriately for your frontend domain
- Use environment variables for all sensitive configuration