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


def create_test_comment(client: TestClient, token: str, post_id: int, content: str = "Test comment", parent_id: int = None):
    """Helper function to create a test comment"""
    comment_data = {
        "content": content,
        "blog_post_id": post_id
    }
    if parent_id:
        comment_data["parent_id"] = parent_id
        
    response = client.post(
        "/comments/",
        json=comment_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    return response.json()


class TestAdvancedCommentSystem:
    def test_create_threaded_comment(self, client):
        """Test creating a threaded comment (reply to another comment)"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        # Create parent comment
        parent_comment = create_test_comment(client, token, post["id"], "Parent comment")
        
        # Create reply comment
        reply_comment = create_test_comment(
            client, token, post["id"], "Reply comment", parent_comment["id"]
        )
        
        assert reply_comment["parent_id"] == parent_comment["id"]
        assert reply_comment["blog_post_id"] == post["id"]
        assert reply_comment["content"] == "Reply comment"

    def test_get_comment_replies(self, client):
        """Test getting replies to a specific comment"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        
        # Create parent comment
        parent_comment = create_test_comment(client, token, post["id"], "Parent comment")
        
        # Create multiple replies
        reply1 = create_test_comment(
            client, token, post["id"], "Reply 1", parent_comment["id"]
        )
        reply2 = create_test_comment(
            client, token, post["id"], "Reply 2", parent_comment["id"]
        )
        
        # Get replies
        response = client.get(
            f"/comments/{parent_comment['id']}/replies",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        replies = response.json()
        assert len(replies) == 2
        assert replies[0]["parent_id"] == parent_comment["id"]
        assert replies[1]["parent_id"] == parent_comment["id"]

    def test_react_to_comment(self, client):
        """Test adding reactions to comments"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        comment = create_test_comment(client, token, post["id"])
        
        # React to comment
        response = client.post(
            f"/comments/{comment['id']}/reactions",
            json={"reaction_type": "like"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["comment_id"] == comment["id"]
        assert data["total_reactions"] == 1
        assert data["reactions_by_type"]["like"] == 1
        assert data["user_reaction"] == "like"

    def test_get_comment_reactions(self, client):
        """Test getting reaction summary for a comment"""
        # Setup
        user1 = create_test_user(client, "user1", "user1@test.com")
        user2 = create_test_user(client, "user2", "user2@test.com")
        
        token1 = get_auth_token(client, "user1")
        token2 = get_auth_token(client, "user2")
        post = create_test_blog_post(client, token1)
        comment = create_test_comment(client, token1, post["id"])
        
        # User 1 likes
        client.post(
            f"/comments/{comment['id']}/reactions",
            json={"reaction_type": "like"},
            headers={"Authorization": f"Bearer {token1}"}
        )
        
        # User 2 loves
        client.post(
            f"/comments/{comment['id']}/reactions",
            json={"reaction_type": "love"},
            headers={"Authorization": f"Bearer {token2}"}
        )
        
        # Get reactions as user 1
        response = client.get(
            f"/comments/{comment['id']}/reactions",
            headers={"Authorization": f"Bearer {token1}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_reactions"] == 2
        assert data["reactions_by_type"]["like"] == 1
        assert data["reactions_by_type"]["love"] == 1
        assert data["user_reaction"] == "like"

    def test_remove_comment_reaction(self, client):
        """Test removing a reaction from a comment"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        comment = create_test_comment(client, token, post["id"])
        
        # React to comment first
        client.post(
            f"/comments/{comment['id']}/reactions",
            json={"reaction_type": "like"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Remove reaction
        response = client.delete(
            f"/comments/{comment['id']}/reactions",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 204
        
        # Check reactions are gone
        response = client.get(
            f"/comments/{comment['id']}/reactions",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_reactions"] == 0
        assert data["user_reaction"] is None

    def test_moderate_comment_hide(self, client):
        """Test hiding a comment through moderation"""
        # Setup
        user1 = create_test_user(client, "author", "author@test.com")
        user2 = create_test_user(client, "commenter", "commenter@test.com")
        
        author_token = get_auth_token(client, "author")
        commenter_token = get_auth_token(client, "commenter")
        
        # Author creates post
        post = create_test_blog_post(client, author_token)
        
        # Commenter creates comment
        comment = create_test_comment(client, commenter_token, post["id"], "Inappropriate comment")
        
        # Author moderates comment (hide)
        response = client.post(
            f"/comments/{comment['id']}/moderate",
            json={"action": "hide", "reason": "Inappropriate content"},
            headers={"Authorization": f"Bearer {author_token}"}
        )
        
        assert response.status_code == 200
        assert "hidden successfully" in response.json()["message"]

    def test_moderate_comment_unauthorized(self, client):
        """Test that only post authors can moderate comments"""
        # Setup
        user1 = create_test_user(client, "author", "author@test.com")
        user2 = create_test_user(client, "commenter", "commenter@test.com")
        user3 = create_test_user(client, "other", "other@test.com")
        
        author_token = get_auth_token(client, "author")
        commenter_token = get_auth_token(client, "commenter")
        other_token = get_auth_token(client, "other")
        
        # Author creates post
        post = create_test_blog_post(client, author_token)
        
        # Commenter creates comment
        comment = create_test_comment(client, commenter_token, post["id"])
        
        # Other user tries to moderate (should fail)
        response = client.post(
            f"/comments/{comment['id']}/moderate",
            json={"action": "hide"},
            headers={"Authorization": f"Bearer {other_token}"}
        )
        
        assert response.status_code == 403
        assert "Not authorized" in response.json()["detail"]

    def test_threaded_comment_validation(self, client):
        """Test validation for threaded comments"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post1 = create_test_blog_post(client, token, "Post 1")
        post2 = create_test_blog_post(client, token, "Post 2")
        
        # Create comment on post1
        comment1 = create_test_comment(client, token, post1["id"])
        
        # Try to create reply that references comment from different post
        response = client.post(
            "/comments/",
            json={
                "content": "Invalid reply",
                "blog_post_id": post2["id"],
                "parent_id": comment1["id"]
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400
        assert "same blog post" in response.json()["detail"]

    def test_comment_reaction_different_types(self, client):
        """Test reacting to comments with different reaction types"""
        # Setup
        user = create_test_user(client)
        token = get_auth_token(client)
        post = create_test_blog_post(client, token)
        comment = create_test_comment(client, token, post["id"])
        
        # Test different reaction types
        reactions = ["like", "love", "laugh", "wow", "sad", "angry"]
        
        for reaction in reactions:
            response = client.post(
                f"/comments/{comment['id']}/reactions",
                json={"reaction_type": reaction},
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 201
            data = response.json()
            assert data["user_reaction"] == reaction

    def test_nonexistent_comment_operations(self, client):
        """Test operations on non-existent comments"""
        user = create_test_user(client)
        token = get_auth_token(client)
        
        # Test getting replies for non-existent comment
        response = client.get(
            "/comments/999999/replies",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404
        
        # Test reacting to non-existent comment
        response = client.post(
            "/comments/999999/reactions",
            json={"reaction_type": "like"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404
        
        # Test moderating non-existent comment
        response = client.post(
            "/comments/999999/moderate",
            json={"action": "hide"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404