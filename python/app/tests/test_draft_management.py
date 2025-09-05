import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.connection import get_db, Base
from app.models.models import User, BlogPost, PostStatus
from app.auth.auth import get_password_hash
import uuid

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_drafts.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    # Clean up test database
    if os.path.exists("./test_drafts.db"):
        os.remove("./test_drafts.db")

@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    try:
        unique_id = str(uuid.uuid4())[:8]
        user = User(
            username=f"testuser_{unique_id}",
            email=f"test_{unique_id}@example.com",
            name="Test User",
            hashed_password=get_password_hash("testpass123")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

@pytest.fixture
def auth_headers(test_user):
    login_data = {
        "username": test_user.username,
        "password": "testpass123"
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

class TestDraftManagement:
    def test_create_draft_post(self, setup_database, auth_headers):
        """Test creating a draft post"""
        post_data = {
            "title": "Draft Post",
            "content": "This is a draft post",
            "status": "DRAFT"
        }
        
        response = client.post("/blog_posts/", json=post_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Draft Post"
        assert data["status"] == "DRAFT"
        assert "slug" in data
    
    def test_create_published_post(self, setup_database, auth_headers):
        """Test creating a published post"""
        post_data = {
            "title": "Published Post",
            "content": "This is a published post",
            "status": "PUBLISHED"
        }
        
        response = client.post("/blog_posts/", json=post_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Published Post"
        assert data["status"] == "PUBLISHED"
    
    def test_create_post_defaults_to_draft(self, setup_database, auth_headers):
        """Test creating post without status defaults to draft"""
        post_data = {
            "title": "Default Status Post",
            "content": "This should be a draft by default"
        }
        
        response = client.post("/blog_posts/", json=post_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "DRAFT"
    
    def test_get_blog_posts_only_shows_published(self, setup_database, auth_headers):
        """Test that GET /blog_posts/ only shows published posts by default"""
        # Create both draft and published posts
        draft_data = {
            "title": "Draft Post",
            "content": "Draft content",
            "status": "DRAFT"
        }
        published_data = {
            "title": "Published Post", 
            "content": "Published content",
            "status": "PUBLISHED"
        }
        
        client.post("/blog_posts/", json=draft_data, headers=auth_headers)
        client.post("/blog_posts/", json=published_data, headers=auth_headers)
        
        # Get all posts (should only show published)
        response = client.get("/blog_posts/")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should only contain published posts
        titles = [post["title"] for post in data]
        assert "Published Post" in titles
        assert "Draft Post" not in titles
    
    def test_get_blog_posts_with_draft_filter(self, setup_database, auth_headers):
        """Test getting blog posts with draft status filter"""
        # Create both draft and published posts
        draft_data = {
            "title": "Another Draft",
            "content": "Draft content",
            "status": "DRAFT"
        }
        published_data = {
            "title": "Another Published",
            "content": "Published content", 
            "status": "PUBLISHED"
        }
        
        client.post("/blog_posts/", json=draft_data, headers=auth_headers)
        client.post("/blog_posts/", json=published_data, headers=auth_headers)
        
        # Get draft posts
        response = client.get("/blog_posts/?status_filter=draft")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should only contain draft posts
        for post in data:
            assert post["status"] == "DRAFT"
    
    def test_get_user_drafts(self, setup_database, auth_headers):
        """Test getting current user's draft posts"""
        # Create some draft posts
        draft_posts = [
            {"title": "Draft 1", "content": "Content 1", "status": "DRAFT"},
            {"title": "Draft 2", "content": "Content 2", "status": "DRAFT"},
            {"title": "Published", "content": "Published content", "status": "PUBLISHED"}
        ]
        
        for post_data in draft_posts:
            client.post("/blog_posts/", json=post_data, headers=auth_headers)
        
        # Get user drafts
        response = client.get("/blog_posts/drafts", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should only contain draft posts
        assert len(data) >= 2
        for post in data:
            assert post["status"] == "DRAFT"
        
        titles = [post["title"] for post in data]
        assert "Draft 1" in titles
        assert "Draft 2" in titles
        assert "Published" not in titles
    
    def test_autosave_draft(self, setup_database, auth_headers):
        """Test auto-saving draft changes"""
        # Create a draft post
        post_data = {
            "title": "Original Title",
            "content": "Original content",
            "status": "DRAFT"
        }
        
        create_response = client.post("/blog_posts/", json=post_data, headers=auth_headers)
        post_id = create_response.json()["id"]
        
        # Auto-save changes
        autosave_data = {
            "title": "Updated Title",
            "content": "Updated content"
        }
        
        response = client.post(f"/blog_posts/{post_id}/autosave", json=autosave_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated content"
        assert data["status"] == "DRAFT"
    
    def test_autosave_published_post_fails(self, setup_database, auth_headers):
        """Test that auto-save fails for published posts"""
        # Create a published post with unique title
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        post_data = {
            "title": f"Published Post for Autosave Test {unique_id}",
            "content": "Published content",
            "status": "PUBLISHED"
        }
        
        create_response = client.post("/blog_posts/", json=post_data, headers=auth_headers)
        assert create_response.status_code == 201, f"Failed to create post: {create_response.text}"
        post_id = create_response.json()["id"]
        
        # Try to auto-save (should fail)
        autosave_data = {
            "title": "Updated Title"
        }
        
        response = client.post(f"/blog_posts/{post_id}/autosave", json=autosave_data, headers=auth_headers)
        
        assert response.status_code == 400
        assert "only available for draft posts" in response.json()["detail"]
    
    def test_publish_draft(self, setup_database, auth_headers):
        """Test publishing a draft post"""
        # Create a draft post
        post_data = {
            "title": "Draft to Publish",
            "content": "This will be published",
            "status": "DRAFT"
        }
        
        create_response = client.post("/blog_posts/", json=post_data, headers=auth_headers)
        post_id = create_response.json()["id"]
        
        # Publish the draft
        response = client.post(f"/blog_posts/{post_id}/publish", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PUBLISHED"
        assert data["title"] == "Draft to Publish"
    
    def test_publish_already_published_post_fails(self, setup_database, auth_headers):
        """Test that publishing an already published post fails"""
        # Create a published post
        post_data = {
            "title": "Already Published",
            "content": "Already published content",
            "status": "PUBLISHED"
        }
        
        create_response = client.post("/blog_posts/", json=post_data, headers=auth_headers)
        post_id = create_response.json()["id"]
        
        # Try to publish again (should fail)
        response = client.post(f"/blog_posts/{post_id}/publish", headers=auth_headers)
        
        assert response.status_code == 400
        assert "Only draft posts can be published" in response.json()["detail"]
    
    def test_update_post_status(self, setup_database, auth_headers):
        """Test updating post status through PUT endpoint"""
        # Create a draft post
        post_data = {
            "title": "Status Test Post",
            "content": "Content",
            "status": "DRAFT"
        }
        
        create_response = client.post("/blog_posts/", json=post_data, headers=auth_headers)
        post_id = create_response.json()["id"]
        
        # Update status to published
        update_data = {
            "status": "PUBLISHED"
        }
        
        response = client.put(f"/blog_posts/{post_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PUBLISHED"
    
    def test_get_drafts_requires_auth(self, setup_database):
        """Test that getting drafts requires authentication"""
        response = client.get("/blog_posts/drafts")
        assert response.status_code == 403
    
    def test_autosave_requires_auth(self, setup_database):
        """Test that auto-save requires authentication"""
        autosave_data = {"title": "Test"}
        response = client.post("/blog_posts/1/autosave", json=autosave_data)
        assert response.status_code == 403