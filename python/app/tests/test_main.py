import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Blog API"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "name": "Test User",
            "password": "TestPass123",
            "retyped_password": "TestPass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data

def test_register_user_password_mismatch():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser2",
            "email": "test2@example.com", 
            "name": "Test User 2",
            "password": "TestPass123",
            "retyped_password": "DifferentPass123"
        }
    )
    assert response.status_code == 400
    assert "Passwords do not match" in response.json()["detail"]

def test_delete_blog_post_not_authenticated():
    """Test that unauthenticated users cannot delete posts"""
    response = client.delete("/blog_posts/1")
    assert response.status_code == 403  # FastAPI returns 403 for missing auth

def test_delete_nonexistent_blog_post():
    """Test deleting a non-existent blog post returns 404"""
    # First register and login a user to get token
    register_response = client.post(
        "/auth/register",
        json={
            "username": "testuser3",
            "email": "test3@example.com",
            "name": "Test User 3", 
            "password": "TestPass123",
            "retyped_password": "TestPass123"
        }
    )
    
    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser3",
            "password": "TestPass123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Try to delete non-existent post
    response = client.delete(
        "/blog_posts/9999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert "Blog post not found" in response.json()["detail"]