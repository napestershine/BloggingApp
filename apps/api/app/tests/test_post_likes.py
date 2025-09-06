import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def create_test_user(client: TestClient, username: str = "testuser", email: str = "test@example.com"):
    """Helper function to create a test user"""
    response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "name": "Test User",
            "password": "testpass123",
            "retyped_password": "testpass123"
        }
    )
    assert response.status_code == 201
    return response.json()


def create_test_blog_post(client: TestClient, token: str, title: str = "Test Post"):
    """Helper function to create a test blog post"""
    response = client.post(
        "/blog_posts/",
        json={
            "title": title,
            "content": "This is a test blog post content.",
            "slug": title.lower().replace(" ", "-")
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    return response.json()


def get_auth_token(client: TestClient, username: str = "testuser", password: str = "testpass123"):
    """Helper function to get authentication token"""
    response = client.post(
        "/auth/login",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


class TestPostLikes:
    def test_like_post_success(self, client):
        """Test successfully liking a post"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        # Like the post
        response = client.post(
            f"/posts/{post['id']}/like",
            json={"reaction_type": "like"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["post_id"] == post["id"]
        assert data["total_reactions"] == 1
        assert data["reactions_by_type"]["like"] == 1
        assert data["user_reaction"] == "like"

    def test_like_post_different_reactions(self, client):
        """Test liking a post with different reaction types"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        # Test different reaction types
        reactions = ["like", "love", "laugh", "wow", "sad", "angry"]
        
        for reaction in reactions:
            response = client.post(
                f"/posts/{post['id']}/like",
                json={"reaction_type": reaction},
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 201
            data = response.json()
            assert data["user_reaction"] == reaction

    def test_update_existing_reaction(self, client):
        """Test updating an existing reaction"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        # First like
        response = client.post(
            f"/posts/{post['id']}/like",
            json={"reaction_type": "like"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        assert response.json()["user_reaction"] == "like"
        
        # Update to love
        response = client.post(
            f"/posts/{post['id']}/like",
            json={"reaction_type": "love"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["user_reaction"] == "love"
        assert data["total_reactions"] == 1  # Should still be 1 total

    def test_unlike_post(self, client):
        """Test removing a like from a post"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        # Like the post first
        response = client.post(
            f"/posts/{post['id']}/like",
            json={"reaction_type": "like"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        
        # Unlike the post
        response = client.delete(
            f"/posts/{post['id']}/like",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 204
        
        # Check reactions are gone
        response = client.get(
            f"/posts/{post['id']}/reactions",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_reactions"] == 0
        assert data["user_reaction"] is None

    def test_get_post_reactions(self, client):
        """Test getting reaction summary for a post"""
        # Setup
        user1 = create_test_user(client, "user1", "user1@test.com")
        user2 = create_test_user(client, "user2", "user2@test.com") 
        
        token1 = get_auth_token(client, "user1")
        token2 = get_auth_token(client, "user2")
        post = create_test_blog_post(client, token1)
        
        # User 1 likes
        client.post(
            f"/posts/{post['id']}/like",
            json={"reaction_type": "like"},
            headers={"Authorization": f"Bearer {token1}"}
        )
        
        # User 2 loves
        client.post(
            f"/posts/{post['id']}/like",
            json={"reaction_type": "love"},
            headers={"Authorization": f"Bearer {token2}"}
        )
        
        # Get reactions as user 1
        response = client.get(
            f"/posts/{post['id']}/reactions",
            headers={"Authorization": f"Bearer {token1}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_reactions"] == 2
        assert data["reactions_by_type"]["like"] == 1
        assert data["reactions_by_type"]["love"] == 1
        assert data["user_reaction"] == "like"

    def test_like_nonexistent_post(self, client):
        """Test liking a post that doesn't exist"""
        user = create_test_user(client)
        token = get_auth_token(client)
        
        response = client.post(
            "/posts/999999/like",
            json={"reaction_type": "like"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404
        assert "Post not found" in response.json()["detail"]

    def test_unlike_nonexistent_like(self, client):
        """Test removing a like that doesn't exist"""
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        response = client.delete(
            f"/posts/{post['id']}/like",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404
        assert "Like not found" in response.json()["detail"]

    def test_unauthorized_access(self, client):
        """Test accessing endpoints without authentication"""
        response = client.post("/posts/1/like", json={"reaction_type": "like"})
        assert response.status_code == 403  # FastAPI returns 403 for missing auth
        
        response = client.delete("/posts/1/like")
        assert response.status_code == 403
        
        response = client.get("/posts/1/reactions")
        assert response.status_code == 403