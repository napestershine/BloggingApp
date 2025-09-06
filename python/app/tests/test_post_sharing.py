import pytest
from fastapi.testclient import TestClient


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


class TestPostSharing:
    def test_share_post_authenticated(self, client):
        """Test sharing a post as an authenticated user"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        # Share the post
        response = client.post(
            f"/posts/{post['id']}/share",
            json={"platform": "twitter"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["post_id"] == post["id"]
        assert data["platform"] == "twitter"
        assert data["user_id"] is not None

    def test_share_post_anonymous(self, client):
        """Test sharing a post as an anonymous user"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        # Share the post without authentication
        response = client.post(
            f"/posts/{post['id']}/share",
            json={"platform": "facebook"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["post_id"] == post["id"]
        assert data["platform"] == "facebook"
        assert data["user_id"] is None

    def test_share_different_platforms(self, client):
        """Test sharing to different platforms"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        platforms = ["twitter", "facebook", "linkedin", "reddit", "email", "copy_link", "whatsapp"]
        
        for platform in platforms:
            response = client.post(
                f"/posts/{post['id']}/share",
                json={"platform": platform},
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 201
            data = response.json()
            assert data["platform"] == platform

    def test_get_post_share_stats(self, client):
        """Test getting share statistics for a post"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        # Share the post multiple times
        client.post(
            f"/posts/{post['id']}/share",
            json={"platform": "twitter"},
            headers={"Authorization": f"Bearer {token}"}
        )
        client.post(
            f"/posts/{post['id']}/share",
            json={"platform": "twitter"}
        )
        client.post(
            f"/posts/{post['id']}/share",
            json={"platform": "facebook"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Get share stats
        response = client.get(f"/posts/{post['id']}/share-stats")
        assert response.status_code == 200
        data = response.json()
        assert data["post_id"] == post["id"]
        assert data["total_shares"] == 3
        assert data["shares_by_platform"]["twitter"] == 2
        assert data["shares_by_platform"]["facebook"] == 1
        assert len(data["recent_shares"]) == 3

    def test_get_post_share_stats_empty(self, client):
        """Test getting share statistics for a post with no shares"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        # Get share stats without any shares
        response = client.get(f"/posts/{post['id']}/share-stats")
        assert response.status_code == 200
        data = response.json()
        assert data["post_id"] == post["id"]
        assert data["total_shares"] == 0
        assert data["shares_by_platform"] == {}
        assert data["recent_shares"] == []

    def test_get_post_shares_with_pagination(self, client):
        """Test getting detailed share records with pagination"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        # Create multiple shares
        for i in range(5):
            client.post(
                f"/posts/{post['id']}/share",
                json={"platform": "twitter"},
                headers={"Authorization": f"Bearer {token}"}
            )
        
        # Get shares with pagination
        response = client.get(f"/posts/{post['id']}/shares?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        # Get next page
        response = client.get(f"/posts/{post['id']}/shares?skip=3&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_post_shares_with_platform_filter(self, client):
        """Test getting shares filtered by platform"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        # Share to different platforms
        client.post(
            f"/posts/{post['id']}/share",
            json={"platform": "twitter"},
            headers={"Authorization": f"Bearer {token}"}
        )
        client.post(
            f"/posts/{post['id']}/share",
            json={"platform": "facebook"},
            headers={"Authorization": f"Bearer {token}"}
        )
        client.post(
            f"/posts/{post['id']}/share",
            json={"platform": "twitter"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Get only Twitter shares
        response = client.get(f"/posts/{post['id']}/shares?platform=twitter")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(share["platform"] == "twitter" for share in data)

    def test_get_popular_sharing_platforms(self, client):
        """Test getting popular sharing platforms"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post1 = create_test_blog_post(client, token, "Post 1")
        post2 = create_test_blog_post(client, token, "Post 2")
        
        # Share posts to different platforms
        for _ in range(3):
            client.post(
                f"/posts/{post1['id']}/share",
                json={"platform": "twitter"},
                headers={"Authorization": f"Bearer {token}"}
            )
        
        for _ in range(2):
            client.post(
                f"/posts/{post2['id']}/share",
                json={"platform": "facebook"},
                headers={"Authorization": f"Bearer {token}"}
            )
        
        client.post(
            f"/posts/{post1['id']}/share",
            json={"platform": "linkedin"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Get popular platforms
        response = client.get("/posts/popular-platforms")
        assert response.status_code == 200
        data = response.json()
        assert data["twitter"] == 3
        assert data["facebook"] == 2
        assert data["linkedin"] == 1

    def test_share_nonexistent_post(self, client):
        """Test sharing a post that doesn't exist"""
        user = create_test_user(client)
        token = get_auth_token(client)
        
        response = client.post(
            "/posts/999999/share",
            json={"platform": "twitter"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404
        assert "Post not found" in response.json()["detail"]

    def test_get_share_stats_nonexistent_post(self, client):
        """Test getting share stats for a post that doesn't exist"""
        response = client.get("/posts/999999/share-stats")
        assert response.status_code == 404
        assert "Post not found" in response.json()["detail"]

    def test_get_shares_nonexistent_post(self, client):
        """Test getting shares for a post that doesn't exist"""
        response = client.get("/posts/999999/shares")
        assert response.status_code == 404
        assert "Post not found" in response.json()["detail"]

    def test_share_invalid_platform(self, client):
        """Test sharing with an invalid platform"""
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        response = client.post(
            f"/posts/{post['id']}/share",
            json={"platform": "invalid_platform"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 422  # Validation error