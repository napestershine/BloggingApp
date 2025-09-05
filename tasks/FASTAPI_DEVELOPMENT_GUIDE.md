# FastAPI Development Guide for Flutter Integration

This guide provides specific instructions for developing FastAPI backend endpoints to support the Flutter blogging app.

## Quick Start

### Running the FastAPI Server
```bash
cd python/
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing APIs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Development Workflow

### 1. API-First Development
1. **Define API endpoint** in the appropriate router file
2. **Create Pydantic models** for request/response validation
3. **Implement database models** if new tables are needed
4. **Write unit tests** for the endpoint
5. **Test manually** using Swagger UI
6. **Update Flutter integration** once API is stable

### 2. FastAPI Project Structure
```
python/
├── app/
│   ├── routers/          # API route handlers
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── users.py      # User management
│   │   ├── blog_posts.py # Blog post CRUD
│   │   └── comments.py   # Comment system
│   ├── models/           # Database models  
│   ├── schemas/          # Pydantic schemas
│   ├── auth/            # Authentication logic
│   ├── database/        # Database connection
│   ├── core/            # Configuration
│   └── tests/           # Test files
├── requirements.txt     # Python dependencies
└── .env                # Environment variables
```

### 3. Adding New Endpoints

#### Step 1: Define Pydantic Models
```python
# schemas/schemas.py
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class Category(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
```

#### Step 2: Create Database Model
```python  
# models/models.py
class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### Step 3: Implement Router
```python
# routers/categories.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[Category])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.post("/", response_model=Category, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
```

#### Step 4: Register Router
```python
# main.py
from app.routers import categories

app.include_router(categories.router)
```

## Flutter Integration Best Practices

### 1. Consistent Response Format
All endpoints should return consistent JSON structure:

```python
# Success Response
{
    "data": {...},           # The actual data
    "message": "Success",    # Human readable message
    "status": "success"      # Status indicator
}

# Error Response  
{
    "detail": "Error message",
    "status": "error",
    "error_code": "VALIDATION_ERROR"
}
```

### 2. Proper HTTP Status Codes
- **200**: Success (GET, PUT)
- **201**: Created (POST)
- **204**: No Content (DELETE)
- **400**: Bad Request (validation errors)
- **401**: Unauthorized (auth required)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found
- **422**: Unprocessable Entity (Pydantic validation)
- **500**: Internal Server Error

### 3. Authentication Implementation
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

def get_current_user(token: str = Depends(security)):
    # Verify JWT token and return user
    pass

@router.get("/protected")
def protected_endpoint(current_user: User = Depends(get_current_user)):
    return {"user": current_user}
```

### 4. Input Validation
```python
from pydantic import BaseModel, validator, Field

class BlogPostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=10)
    category_id: Optional[int] = None
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
```

### 5. Error Handling
```python
from fastapi import HTTPException, status

@router.get("/blog_posts/{post_id}")
def get_blog_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )
    return post
```

## Testing Guidelines

### 1. Unit Testing
```python
# tests/test_blog_posts.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_blog_post():
    response = client.post("/blog_posts/", json={
        "title": "Test Post",
        "content": "Test content"
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"

def test_get_nonexistent_post():
    response = client.get("/blog_posts/999")
    assert response.status_code == 404
```

### 2. Running Tests
```bash
cd python/
python -m pytest app/tests/ -v
```

## Performance Considerations

### 1. Database Queries
- Use proper indexes on frequently queried columns
- Implement pagination for list endpoints
- Use eager loading for related data

### 2. Caching
- Cache expensive queries
- Use Redis for session storage
- Implement proper cache invalidation

### 3. File Uploads
```python
from fastapi import File, UploadFile

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type and size
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Invalid file type")
    
    # Save file and return URL
    return {"url": file_url}
```

## Security Checklist

- [ ] Input validation on all endpoints
- [ ] Authentication required for protected routes
- [ ] Rate limiting implemented
- [ ] CORS properly configured
- [ ] SQL injection prevention (use SQLAlchemy)
- [ ] File upload validation
- [ ] Secure password hashing
- [ ] Environment variables for secrets
- [ ] HTTPS in production

## Deployment Considerations

### Environment Variables
```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost/blogdb
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Production Setup
- Use PostgreSQL instead of SQLite
- Set up proper logging
- Configure reverse proxy (nginx)
- Use process manager (gunicorn)
- Set up monitoring and alerting
- Implement proper backup strategy

## Next Priority Endpoints

Based on Flutter development needs, implement in this order:

1. **P0 Critical**:
   - `DELETE /blog_posts/{id}`
   - `DELETE /comments/{id}`  
   - `POST /auth/verify-email`
   - `POST /auth/password/reset`

2. **P1 High Priority**:
   - `POST /media/upload`
   - `GET /search`
   - `POST /blog_posts/{id}/like`
   - `GET /categories`

3. **P2 Medium Priority**:
   - `GET /notifications`
   - `POST /users/{id}/follow`
   - `GET /blog_posts/trending`