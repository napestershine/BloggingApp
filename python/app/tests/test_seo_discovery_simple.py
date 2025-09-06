import pytest
from app.models.models import User, BlogPost
from app.auth.auth import get_password_hash, create_access_token
import json

def test_search_posts_basic(client, test_db):
    """Test basic search functionality"""
    # Create test data
    db = test_db()
    
    # Create test user
    user = User(
        username="testuser",
        email="test@example.com",
        name="Test User",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create test post
    post = BlogPost(
        title="Introduction to Python Programming",
        content="Python is a powerful programming language for beginners...",
        slug="intro-python",
        author_id=user.id,
        category="technology",
        tags='["python", "programming"]',
        view_count=100
    )
    db.add(post)
    db.commit()
    db.close()
    
    # Test search
    response = client.get("/api/search/?q=python")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "posts" in data
    assert "total" in data
    assert "suggestions" in data

def test_search_with_filters(client, test_db):
    """Test search with category filter"""
    # Create test data
    db = test_db()
    
    user = User(
        username="testuser2",
        email="test2@example.com",
        name="Test User 2",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    post = BlogPost(
        title="Tech Tutorial",
        content="Technology content here...",
        slug="tech-tutorial",
        author_id=user.id,
        category="technology"
    )
    db.add(post)
    db.commit()
    db.close()
    
    response = client.get("/api/search/?q=&category=technology")
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data

def test_search_suggestions(client, test_db):
    """Test search suggestions"""
    response = client.get("/api/search/suggestions?q=tech")
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "suggestions" in data

def test_search_filters_endpoint(client):
    """Test search filters endpoint"""
    response = client.get("/api/search/filters")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert "authors" in data
    assert "tags" in data

def test_seo_get_post_seo(client, test_db):
    """Test getting SEO data for a post"""
    # Create test data
    db = test_db()
    
    user = User(
        username="seouser",
        email="seo@example.com",
        name="SEO User",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    post = BlogPost(
        title="SEO Test Post",
        content="Content for SEO testing...",
        slug="seo-test",
        author_id=user.id,
        meta_title="SEO Meta Title",
        meta_description="SEO meta description"
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    post_id = post.id
    db.close()
    
    response = client.get(f"/api/seo/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["meta_title"] == "SEO Meta Title"
    assert data["meta_description"] == "SEO meta description"

def test_seo_update_post_seo(client, test_db):
    """Test updating SEO data"""
    # Create test data
    db = test_db()
    
    user = User(
        username="seoupdateuser",
        email="seoupdate@example.com",
        name="SEO Update User",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    post = BlogPost(
        title="SEO Update Test",
        content="Content...",
        slug="seo-update-test",
        author_id=user.id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    post_id = post.id
    username = user.username  # Get username before closing db
    db.close()
    
    # Create token
    token = create_access_token(data={"sub": username})
    
    seo_data = {
        "meta_title": "Updated Meta Title",
        "meta_description": "Updated meta description"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(f"/api/seo/posts/{post_id}", json=seo_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["meta_title"] == "Updated Meta Title"

def test_seo_preview(client, test_db):
    """Test SEO preview generation"""
    # Create test data
    db = test_db()
    
    user = User(
        username="previewuser",
        email="preview@example.com",
        name="Preview User",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    post = BlogPost(
        title="Preview Test Post",
        content="Content for preview testing...",
        slug="preview-test",
        author_id=user.id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    post_id = post.id
    db.close()
    
    response = client.get(f"/api/seo/posts/{post_id}/preview")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "description" in data
    assert "url" in data

def test_seo_validation(client):
    """Test SEO data validation"""
    seo_data = {
        "meta_title": "Good Title",
        "meta_description": "Good description that is the right length for SEO purposes and provides value"
    }
    
    response = client.post("/api/seo/validate", json=seo_data)
    assert response.status_code == 200
    data = response.json()
    assert "issues" in data
    assert "recommendations" in data
    assert "score" in data

def test_sitemap_xml(client, test_db):
    """Test XML sitemap generation"""
    response = client.get("/api/sitemap.xml")
    assert response.status_code == 200
    assert "application/xml" in response.headers["content-type"]
    assert "<?xml" in response.text

def test_sitemap_posts(client):
    """Test sitemap posts JSON"""
    response = client.get("/api/sitemap/posts")
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
    assert "generated_at" in data

def test_robots_txt(client):
    """Test robots.txt generation"""
    response = client.get("/api/robots.txt")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "User-agent: *" in response.text

def test_slug_validation(client):
    """Test slug validation"""
    response = client.get("/api/slugs/validate?slug=test-unique-slug")
    assert response.status_code == 200
    data = response.json()
    assert "slug" in data
    assert "is_available" in data
    assert "suggestions" in data

def test_slug_suggestions(client):
    """Test slug suggestions"""
    response = client.get("/api/slugs/suggest?title=How to Learn Programming")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "suggestions" in data

def test_trending_posts(client):
    """Test trending posts"""
    response = client.get("/api/posts/trending")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_hot_topics(client):
    """Test hot topics"""
    response = client.get("/api/topics/hot")
    assert response.status_code == 200
    data = response.json()
    assert "hot_topics" in data

def test_rss_feed(client):
    """Test RSS feed"""
    response = client.get("/api/rss/")
    assert response.status_code == 200
    assert "application/rss+xml" in response.headers["content-type"]
    assert "<?xml" in response.text

def test_category_rss_feed(client):
    """Test category RSS feed"""
    response = client.get("/api/rss/categories/technology")
    assert response.status_code == 200
    assert "application/rss+xml" in response.headers["content-type"]

def test_related_posts(client, test_db):
    """Test related posts"""
    # Create test data
    db = test_db()
    
    user = User(
        username="relateduser",
        email="related@example.com",
        name="Related User",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    post = BlogPost(
        title="Test Post for Related",
        content="Content...",
        slug="test-related",
        author_id=user.id,
        category="technology"
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    post_id = post.id
    db.close()
    
    response = client.get(f"/api/posts/{post_id}/related")
    assert response.status_code == 200
    assert isinstance(response.json(), list)