import pytest
from app.models.models import User, BlogPost
from app.auth.auth import get_password_hash, create_access_token

def test_personalized_feed_requires_auth(client):
    """Test that personalized feed requires authentication"""
    response = client.get("/api/feed/personalized")
    assert response.status_code == 403  # FastAPI returns 403 for missing auth

def test_personalized_feed_with_auth(client, test_db):
    """Test personalized feed with authentication"""
    # Create test data
    db = test_db()
    
    user = User(
        username="feeduser",
        email="feed@example.com",
        name="Feed User",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    post = BlogPost(
        title="Feed Test Post",
        content="Content for feed testing...",
        slug="feed-test",
        author_id=user.id,
        view_count=50
    )
    db.add(post)
    db.commit()
    username = user.username  # Get username before closing db
    db.close()
    
    # Create token and test
    token = create_access_token(data={"sub": username})
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/feed/personalized", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_user_interests_requires_auth(client):
    """Test that user interests require authentication"""
    response = client.get("/api/feed/user/interests")
    assert response.status_code == 403  # FastAPI returns 403 for missing auth

def test_get_user_interests(client, test_db):
    """Test getting user interests"""
    # Create test data
    db = test_db()
    
    user = User(
        username="interestuser",
        email="interest@example.com",
        name="Interest User",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    username = user.username  # Get username before closing db
    db.close()
    
    token = create_access_token(data={"sub": username})
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/feed/user/interests", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "interests" in data
    assert "recommendations" in data

def test_update_user_interests(client, test_db):
    """Test updating user interests"""
    # Create test data
    db = test_db()
    
    user = User(
        username="updateuser",
        email="update@example.com",
        name="Update User",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    username = user.username  # Get username before closing db
    db.close()
    
    token = create_access_token(data={"sub": username})
    headers = {"Authorization": f"Bearer {token}"}
    
    interests = {
        "categories": ["technology", "programming"],
        "tags": ["python", "javascript"]
    }
    
    response = client.put("/api/feed/user/interests", json=interests, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "updated_interests" in data
    assert data["updated_interests"] == interests