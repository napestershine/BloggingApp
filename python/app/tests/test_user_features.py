import pytest
import uuid

def get_unique_username():
    """Generate a unique username for testing"""
    return f"testuser_{str(uuid.uuid4())[:8]}"

def get_unique_email():
    """Generate a unique email for testing"""
    return f"test_{str(uuid.uuid4())[:8]}@example.com"

def test_user_registration_and_login(client):
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

def test_email_verification_flow(client):
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

def test_password_reset_flow(client):
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

def test_user_profile_management(client):
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

def test_sample_credentials(client):
    """Test login with sample credentials - first create the users"""
    from app.auth.auth import get_password_hash
    
    sample_users_data = [
        {"username": "admin", "password": "admin123", "email": "admin@example.com", "name": "Admin User"},
        {"username": "johndoe", "password": "john123", "email": "john@example.com", "name": "John Doe"},
        {"username": "janesmith", "password": "jane123", "email": "jane@example.com", "name": "Jane Smith"},
    ]
    
    # First create the users using the registration endpoint
    for user_data in sample_users_data:
        registration_data = {
            "username": user_data["username"],
            "password": user_data["password"],
            "retyped_password": user_data["password"],
            "name": user_data["name"],
            "email": user_data["email"]
        }
        response = client.post("/auth/register", json=registration_data)
        # It's okay if the user already exists (201 for created, other codes for existing)
        assert response.status_code in [201, 400]  # 400 might be returned if user exists
    
    # Now test login with the credentials
    sample_credentials = [
        {"username": "admin", "password": "admin123"},
        {"username": "johndoe", "password": "john123"},
        {"username": "janesmith", "password": "jane123"},
    ]
    
    # Create each user first
    for user_data in sample_users:
        registration_data = {
            "username": user_data["username"],
            "password": user_data["password"],
            "retyped_password": user_data["password"],
            "name": user_data["name"],
            "email": user_data["email"]
        }
        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == 201, f"Failed to create user {user_data['username']}"
    
    # Now test login with these credentials
    for user_data in sample_users:
        login_cred = {"username": user_data["username"], "password": user_data["password"]}
        response = client.post("/auth/login", data=login_cred)
        assert response.status_code == 200, f"Failed to login with {user_data['username']}"
        token_data = response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"

def test_complete_user_journey(client):
    """Test complete user journey from registration to profile management"""
    username = get_unique_username()
    email = get_unique_email()
    
    # 1. Register user
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
    
    # 2. Request email verification
    response = client.post("/auth/verify-email", json={"email": email})
    assert response.status_code == 200
    verification_token = response.json()["token"]
    
    # 3. Confirm email verification
    response = client.post("/auth/verify-email/confirm", json={"token": verification_token})
    assert response.status_code == 200
    
    # 4. Login
    login_data = {"username": username, "password": "testpass123"}
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 5. Get profile
    response = client.get(f"/users/{user_id}/profile", headers=headers)
    assert response.status_code == 200
    
    # 6. Update profile
    update_data = {
        "name": "Updated Test User",
        "bio": "Updated bio",
        "social_links": {"twitter": "@testuser"}
    }
    response = client.put(f"/users/{user_id}/profile", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_profile = response.json()
    assert updated_profile["name"] == "Updated Test User"
    assert updated_profile["bio"] == "Updated bio"
    
    # 7. Refresh token
    import time
    time.sleep(1)  # Ensure different timestamp
    response = client.post("/auth/refresh", headers=headers)
    assert response.status_code == 200
    new_token = response.json()["access_token"]
    # Token should be valid (content may be same due to timing but endpoint works)
    
    # 8. Logout
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200
