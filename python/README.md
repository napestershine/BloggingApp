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

1. Install Python 3.13+ and create a virtual environment:
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

### Database Seeding

The application includes a comprehensive seeding system for development and testing. The seeder creates sample data including users, blog posts, and comments.

#### CLI Commands

```bash
# Seed the database with sample data (idempotent)
python seed.py up

# Check seeding status
python seed.py status

# Clear seeded data
python seed.py down

# Reset (clear and re-seed)
python seed.py reset

# Seed with demo data
python seed.py demo
```

#### Docker Integration

You can automatically seed the database when starting the Docker container by setting the `SEED_ON_START` environment variable:

```bash
# docker-compose.yml or environment variables
SEED_ON_START=true
```

Or run it manually in Docker:
```bash
docker compose exec python python seed.py up
```

#### Sample Credentials

After seeding, you can use these credentials to test the application:

- **Admin**: `admin` / `admin123`
- **Editor**: `editor` / `editor123`  
- **User**: `user1` / `user123`

#### Test Fixtures

For automated testing, the seeding system provides pytest fixtures:

```python
def test_with_seed_data(seed_data):
    # Full seed data including users, posts, comments
    admin_user = seed_data["admin_user"]
    welcome_post = seed_data["welcome_post"]
    
def test_with_minimal_data(minimal_seed_data):
    # Minimal data for lightweight tests
    admin_user = minimal_seed_data["admin_user"]
    test_post = minimal_seed_data["test_post"]
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

## Database Management

### Schema Migrations

**Schema is managed exclusively by Alembic migrations - NOT by `Base.metadata.create_all()`**

Before running the application for the first time, apply migrations:

```bash
# Apply all pending migrations
alembic upgrade head

# Create a new migration (after schema changes)
alembic revision --autogenerate -m "Description of changes"

# Review migration before committing
# Run in a test environment first
```

**Important**: The application will not auto-create schema. Always run migrations first.

### Notifications & Follows System

The notifications and follows system is hardened for production use with:

#### Performance Optimizations

- **N+1 Query Prevention**: Uses SQLAlchemy `joinedload()` eager loading
  - Fetches 100+ notifications in only 2-3 queries (verified by tests)
  - Related users and posts are loaded in single query pass
  
- **Indexed Queries**:
  - Composite index on `(user_id, created_at DESC)` for efficient notification retrieval
  - Partial index on unread notifications (`WHERE is_read = false`) for fast unread queries
  - Indexes on `(follower_id, following_id)` for efficient follow lookups

#### Data Integrity

- **Cascade Deletes**: `ON DELETE CASCADE` on all notification/follow relationships
  - Deleting a user automatically removes their notifications and follows
  - Prevents orphaned records
  
- **Unique Constraints**:
  - `UNIQUE (follower_id, following_id)` prevents duplicate follows
  - `UNIQUE (user_id, blog_post_id)` for bookmarks
  
- **Transactional Safety**:
  - Follow + notification creation is atomic
  - If notification fails, follow is rolled back
  - No partial state in database

#### Bulk Operation Safety

- **Limits**: `DELETE` limits capped at 1000 per operation (prevent accidental data loss)
- **Per-User Scoping**: All bulk operations scoped to `current_user.id` (security)
- **Logging**: Bulk operations logged for audit trail
- **Response**: Returns count of affected rows

Example: Mark all notifications as read (scoped to current user, limited count returned):
```python
# Request
PATCH /notifications/read-all

# Response
{
  "message": "Marked 25 notifications as read",
  "count": 25
}
```

#### SQLAlchemy Best Practices

- Uses `.is_()` for boolean comparisons (not `== True/False`)
- Uses `synchronize_session=False` for bulk operations (performance)
- Uses `select()` and modern 2.x API patterns
- Proper foreign key constraints with `ondelete='CASCADE'`

#### Response Models

All endpoints return Pydantic models (not raw dicts) for:
- Type safety and validation
- OpenAPI schema generation
- Consistent API contracts

Example response:
```json
{
  "id": 1,
  "user_id": 42,
  "type": "follow",
  "title": "New Follower",
  "message": "Alice started following you",
  "is_read": false,
  "created_at": "2025-02-28T12:00:00+00:00",
  "read_at": null,
  "related_user_id": 10,
  "related_user": {
    "id": 10,
    "username": "alice",
    "name": "Alice"
  },
  "related_post_id": null,
  "related_comment_id": null,
  "related_post": null
}
```

#### Enum Alignment

Notification types are consistent across Python (Pydantic), database, and API clients:

```python
class NotificationType(enum.Enum):
    FOLLOW = "follow"
    POST_LIKE = "post_like"
    POST_COMMENT = "post_comment"
    POST_SHARE = "post_share"
    COMMENT_LIKE = "comment_like"
    COMMENT_REPLY = "comment_reply"
    MENTION = "mention"
    SYSTEM = "system"
```

These values are:
- Persisted in the database as strings
- Exposed in OpenAPI schema
- Used for TypeScript client generation (via OpenAPI)
- Available in Flutter generated models

## Security Notes

- Change the `SECRET_KEY` in production
- Use HTTPS in production
- Configure CORS appropriately for your frontend domain
- Use environment variables for all sensitive configuration
