import pytest
from app.models.models import User, Category, Tag, BlogPost
from app.auth.auth import get_password_hash
import uuid

@pytest.fixture
def test_user(test_db):
    db = test_db()
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
def auth_headers(test_user, client):
    login_data = {
        "username": test_user.username,
        "password": "testpass123"
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

class TestCategories:
    def test_create_category(self, auth_headers, client):
        """Test creating a new category"""
        category_data = {
            "name": "Technology",
            "description": "Posts about technology and programming"
        }
        
        response = client.post("/categories/", json=category_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Technology"
        assert data["description"] == "Posts about technology and programming"
        assert data["slug"] == "technology"
        assert "id" in data
    
    def test_create_category_custom_slug(self, auth_headers, client):
        """Test creating category with custom slug"""
        category_data = {
            "name": "Web Development",
            "description": "Web dev posts",
            "slug": "webdev"
        }
        
        response = client.post("/categories/", json=category_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["slug"] == "webdev"
    
    def test_create_duplicate_category(self, auth_headers, client):
        """Test creating category with duplicate name should fail"""
        category_data = {
            "name": "Duplicate Category",
            "description": "First category"
        }
        
        # Create first category
        response1 = client.post("/categories/", json=category_data, headers=auth_headers)
        assert response1.status_code == 201
        
        # Try to create duplicate
        response2 = client.post("/categories/", json=category_data, headers=auth_headers)
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"]
    
    def test_get_categories(self, auth_headers, client):
        """Test getting list of categories"""
        # Create a few categories
        categories = [
            {"name": "Science", "description": "Science posts"},
            {"name": "Travel", "description": "Travel posts"}
        ]
        
        for cat_data in categories:
            client.post("/categories/", json=cat_data, headers=auth_headers)
        
        response = client.get("/categories/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        category_names = [cat["name"] for cat in data]
        assert "Science" in category_names
        assert "Travel" in category_names
    
    def test_get_category_by_id(self, auth_headers, client):
        """Test getting a specific category by ID"""
        category_data = {
            "name": "Specific Category",
            "description": "A specific category"
        }
        
        create_response = client.post("/categories/", json=category_data, headers=auth_headers)
        category_id = create_response.json()["id"]
        
        response = client.get(f"/categories/{category_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Specific Category"
    
    def test_update_category(self, auth_headers, client):
        """Test updating a category"""
        # Create category
        category_data = {
            "name": "Original Name",
            "description": "Original description"
        }
        
        create_response = client.post("/categories/", json=category_data, headers=auth_headers)
        category_id = create_response.json()["id"]
        
        # Update category
        update_data = {
            "name": "Updated Name",
            "description": "Updated description"
        }
        
        response = client.put(f"/categories/{category_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["description"] == "Updated description"
    
    def test_delete_category(self, auth_headers, client):
        """Test deleting a category"""
        category_data = {
            "name": "To Be Deleted",
            "description": "This will be deleted"
        }
        
        create_response = client.post("/categories/", json=category_data, headers=auth_headers)
        category_id = create_response.json()["id"]
        
        # Delete category
        response = client.delete(f"/categories/{category_id}", headers=auth_headers)
        assert response.status_code == 204
        
        # Verify category is gone
        get_response = client.get(f"/categories/{category_id}")
        assert get_response.status_code == 404

class TestTags:
    def test_create_tag(self, auth_headers, client):
        """Test creating a new tag"""
        tag_data = {"name": "Python"}
        
        response = client.post("/tags/", json=tag_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "python"  # Should be lowercase
        assert "id" in data
    
    def test_create_duplicate_tag_returns_existing(self, auth_headers, client):
        """Test creating duplicate tag returns existing tag"""
        tag_data = {"name": "JavaScript"}
        
        # Create first tag
        response1 = client.post("/tags/", json=tag_data, headers=auth_headers)
        assert response1.status_code == 201
        tag1_id = response1.json()["id"]
        
        # Create duplicate (should return existing)
        response2 = client.post("/tags/", json=tag_data, headers=auth_headers)
        assert response2.status_code == 201
        tag2_id = response2.json()["id"]
        
        # Should be the same tag
        assert tag1_id == tag2_id
    
    def test_get_tags(self, auth_headers, client):
        """Test getting list of tags"""
        tags = ["React", "Vue", "Angular"]
        
        for tag_name in tags:
            client.post("/tags/", json={"name": tag_name}, headers=auth_headers)
        
        response = client.get("/tags/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        tag_names = [tag["name"] for tag in data]
        assert "react" in tag_names
        assert "vue" in tag_names
        assert "angular" in tag_names
    
    def test_search_tags(self, auth_headers, client):
        """Test searching tags"""
        tags = ["Machine Learning", "Machine Vision", "Deep Learning"]
        
        for tag_name in tags:
            client.post("/tags/", json={"name": tag_name}, headers=auth_headers)
        
        response = client.get("/tags/search/machine")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        tag_names = [tag["name"] for tag in data]
        assert "machine learning" in tag_names
        assert "machine vision" in tag_names
    
    def test_delete_tag(self, auth_headers, client):
        """Test deleting a tag"""
        tag_data = {"name": "ToDelete"}
        
        create_response = client.post("/tags/", json=tag_data, headers=auth_headers)
        tag_id = create_response.json()["id"]
        
        # Delete tag
        response = client.delete(f"/tags/{tag_id}", headers=auth_headers)
        assert response.status_code == 204
        
        # Verify tag is gone
        get_response = client.get(f"/tags/{tag_id}")
        assert get_response.status_code == 404

class TestBlogPostTagsCategories:
    def test_assign_tags_to_blog_post(self, auth_headers, client):
        """Test assigning tags to a blog post"""
        # Create tags
        tag1_response = client.post("/tags/", json={"name": "Python"}, headers=auth_headers)
        tag2_response = client.post("/tags/", json={"name": "FastAPI"}, headers=auth_headers)
        tag1_id = tag1_response.json()["id"]
        tag2_id = tag2_response.json()["id"]
        
        # Create blog post
        post_data = {
            "title": "Test Post",
            "content": "This is a test post"
        }
        post_response = client.post("/blog_posts/", json=post_data, headers=auth_headers)
        post_id = post_response.json()["id"]
        
        # Assign tags to post
        tags_update = {"tag_ids": [tag1_id, tag2_id]}
        response = client.put(f"/blog_posts/{post_id}/tags", json=tags_update, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        tag_names = [tag["name"] for tag in data]
        assert "python" in tag_names
        assert "fastapi" in tag_names
    
    def test_assign_categories_to_blog_post(self, auth_headers, client):
        """Test assigning categories to a blog post"""
        # Create categories
        cat1_response = client.post("/categories/", json={"name": "Programming"}, headers=auth_headers)
        cat2_response = client.post("/categories/", json={"name": "Tutorial"}, headers=auth_headers)
        cat1_id = cat1_response.json()["id"]
        cat2_id = cat2_response.json()["id"]
        
        # Create blog post
        post_data = {
            "title": "Test Post with Categories",
            "content": "This is a test post with categories"
        }
        post_response = client.post("/blog_posts/", json=post_data, headers=auth_headers)
        post_id = post_response.json()["id"]
        
        # Assign categories to post
        categories_update = {"category_ids": [cat1_id, cat2_id]}
        response = client.put(f"/blog_posts/{post_id}/categories", json=categories_update, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        category_names = [cat["name"] for cat in data]
        assert "Programming" in category_names
        assert "Tutorial" in category_names
    
    def test_get_blog_post_tags(self, auth_headers, client):
        """Test getting tags for a blog post"""
        # Create tag and blog post with tag
        tag_response = client.post("/tags/", json={"name": "TestTag"}, headers=auth_headers)
        tag_id = tag_response.json()["id"]
        
        post_data = {"title": "Post with Tag", "content": "Content"}
        post_response = client.post("/blog_posts/", json=post_data, headers=auth_headers)
        post_id = post_response.json()["id"]
        
        # Assign tag
        client.put(f"/blog_posts/{post_id}/tags", json={"tag_ids": [tag_id]}, headers=auth_headers)
        
        # Get tags
        response = client.get(f"/blog_posts/{post_id}/tags")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "testtag"