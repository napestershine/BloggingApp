import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def get_unique_username():
    """Generate a unique username for testing"""
    return f"testuser_{str(uuid.uuid4())[:8]}"

def get_unique_email():
    """Generate a unique email for testing"""
    return f"test_{str(uuid.uuid4())[:8]}@example.com"

def test_user_registration_and_login():
    """Test complete user registration and login flow"""
    username = get_unique_username()
    email = get_unique_email()
    
    # Test registration
    registration_data = {
        "username": username,
        "password": "testpass123",
        "retyped_password": "testpass123",
        "name": "Test User",
        "email": email
    }
    
    response = client.post("/auth/register", json=registration_data)
    assert response.status_code == 201
    user_data = response.json()
    assert user_data["username"] == username
    assert user_data["email"] == email
    
    # Test login
    login_data = {
        "username": username,
        "password": "testpass123"
    }
    
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_email_verification_flow():
    """Test email verification flow"""
    username = get_unique_username()
    email = get_unique_email()
    
    # First register a user
    registration_data = {
        "username": username,
        "password": "testpass123",
        "retyped_password": "testpass123",
        "name": "Test User",
        "email": email
    }
    response = client.post("/auth/register", json=registration_data)
    assert response.status_code == 201
    
    # Request email verification
    response = client.post("/auth/verify-email", json={"email": email})
    assert response.status_code == 200
    verification_data = response.json()
    assert "token" in verification_data
    
    # Confirm email verification
    token = verification_data["token"]
    response = client.post("/auth/verify-email/confirm", json={"token": token})
    assert response.status_code == 200
    assert response.json()["message"] == "Email verified successfully"

def test_password_reset_flow():
    """Test password reset flow"""
    username = get_unique_username()
    email = get_unique_email()
    
    # First register a user
    registration_data = {
        "username": username,
        "password": "testpass123",
        "retyped_password": "testpass123",
        "name": "Test User",
        "email": email
    }
    response = client.post("/auth/register", json=registration_data)
    assert response.status_code == 201
    
    # Request password reset
    response = client.post("/auth/password/forgot", json={"email": email})
    assert response.status_code == 200
    reset_data = response.json()
    assert "token" in reset_data
    
    # Reset password
    token = reset_data["token"]
    response = client.post("/auth/password/reset", json={
        "token": token,
        "new_password": "newpassword456"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Password reset successfully"
    
    # Test login with new password
    login_data = {
        "username": username,
        "password": "newpassword456"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200

def test_user_profile_management():
    """Test user profile management"""
    username = get_unique_username()
    email = get_unique_email()
    
    # First register a user
    registration_data = {
        "username": username,
        "password": "testpass123",
        "retyped_password": "testpass123",
        "name": "Test User",
        "email": email
    }
    response = client.post("/auth/register", json=registration_data)
    assert response.status_code == 201
    user_data = response.json()
    user_id = user_data["id"]
    
    # Login to get token
    login_data = {
        "username": username,
        "password": "testpass123"
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get user profile
    response = client.get(f"/users/{user_id}/profile", headers=headers)
    assert response.status_code == 200
    profile_data = response.json()
    assert profile_data["username"] == username
    
    # Update user profile
    update_data = {
        "name": "Updated Test User",
        "bio": "This is my test bio",
        "social_links": {
            "twitter": "@testuser",
            "github": "github.com/testuser"
        }
    }
    response = client.put(f"/users/{user_id}/profile", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_profile = response.json()
    assert updated_profile["name"] == "Updated Test User"
    assert updated_profile["bio"] == "This is my test bio"
    assert updated_profile["social_links"]["twitter"] == "@testuser"

def test_unauthorized_profile_access():
    """Test that users cannot update other users' profiles without permission"""
    # Profile viewing should be public (no authentication required)
    response = client.get("/users/1/profile")
    assert response.status_code == 200  # Public profile access should work
    
    # Try to update profile without token - this should fail
    response = client.put("/users/1/profile", json={"name": "Hacker"})
    assert response.status_code in [401, 403]  # Either unauthorized or forbidden is acceptable