import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.models import User, BlogPost, Bookmark


class TestBookmarkEndpoints:
    """Test suite for bookmark functionality."""

    def create_test_data(self, db):
        """Helper to create test user and posts."""
        user = User(
            username="testuser",
            email="test@example.com",
            name="Test User",
            hashed_password="hashed"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        post1 = BlogPost(
            title="How to Learn Python",
            content="A comprehensive guide to learning Python programming",
            slug="how-to-learn-python",
            author_id=user.id
        )
        post2 = BlogPost(
            title="Web Development with FastAPI",
            content="Building modern web applications with FastAPI",
            slug="web-development-fastapi",
            author_id=user.id
        )
        db.add(post1)
        db.add(post2)
        db.commit()
        db.refresh(post1)
        db.refresh(post2)
        
        return user, post1, post2

    def test_bookmark_post_success(self, client: TestClient, test_db):
        """Test successfully bookmarking a post."""
        db = test_db()
        user, post1, _ = self.create_test_data(db)
        db.close()

        # Bookmark the post
        response = client.post(f"/bookmarks/posts/{post1.id}", json={"user_id": user.id})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Post bookmarked successfully"
        assert data["user_id"] == user.id
        assert data["post_id"] == post1.id

    def test_bookmark_post_already_bookmarked(self, client: TestClient, test_db):
        """Test bookmarking a post that's already bookmarked."""
        db = test_db()
        user, post1, _ = self.create_test_data(db)
        
        # Create existing bookmark
        bookmark = Bookmark(user_id=user.id, post_id=post1.id)
        db.add(bookmark)
        db.commit()
        db.close()

        # Try to bookmark again
        response = client.post(f"/bookmarks/posts/{post1.id}", json={"user_id": user.id})
        assert response.status_code == 400
        data = response.json()
        assert "already bookmarked" in data["detail"].lower()

    def test_bookmark_nonexistent_post(self, client: TestClient, test_db):
        """Test bookmarking a post that doesn't exist."""
        db = test_db()
        user, _, _ = self.create_test_data(db)
        db.close()

        # Try to bookmark non-existent post
        response = client.post("/bookmarks/posts/99999", json={"user_id": user.id})
        assert response.status_code == 404
        data = response.json()
        assert "post not found" in data["detail"].lower()

    def test_bookmark_by_nonexistent_user(self, client: TestClient, test_db):
        """Test bookmarking by a user that doesn't exist."""
        db = test_db()
        _, post1, _ = self.create_test_data(db)
        db.close()

        # Try to bookmark with non-existent user
        response = client.post(f"/bookmarks/posts/{post1.id}", json={"user_id": 99999})
        assert response.status_code == 404
        data = response.json()
        assert "user not found" in data["detail"].lower()

    def test_unbookmark_post_success(self, client: TestClient, test_db):
        """Test successfully removing a bookmark."""
        db = test_db()
        user, post1, _ = self.create_test_data(db)
        
        # Create bookmark
        bookmark = Bookmark(user_id=user.id, post_id=post1.id)
        db.add(bookmark)
        db.commit()
        db.close()

        # Remove bookmark
        response = client.delete(f"/bookmarks/posts/{post1.id}?user_id={user.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Bookmark removed successfully"

    def test_unbookmark_post_not_bookmarked(self, client: TestClient, test_db):
        """Test removing a bookmark that doesn't exist."""
        db = test_db()
        user, post1, _ = self.create_test_data(db)
        db.close()

        # Try to remove non-existent bookmark
        response = client.delete(f"/bookmarks/posts/{post1.id}?user_id={user.id}")
        assert response.status_code == 404
        data = response.json()
        assert "bookmark not found" in data["detail"].lower()

    def test_get_user_bookmarks(self, client: TestClient, test_db):
        """Test getting a user's bookmarks."""
        db = test_db()
        user, post1, post2 = self.create_test_data(db)
        
        # Create bookmarks
        bookmark1 = Bookmark(user_id=user.id, post_id=post1.id)
        bookmark2 = Bookmark(user_id=user.id, post_id=post2.id)
        db.add(bookmark1)
        db.add(bookmark2)
        db.commit()
        db.close()

        # Get user's bookmarks
        response = client.get(f"/bookmarks/users/{user.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["bookmarks"]) == 2
        assert data["total"] == 2
        
        # Check that posts are included in response
        titles = [bookmark["post"]["title"] for bookmark in data["bookmarks"]]
        assert "How to Learn Python" in titles
        assert "Web Development with FastAPI" in titles

    def test_get_user_bookmarks_empty(self, client: TestClient, test_db):
        """Test getting bookmarks for user with no bookmarks."""
        db = test_db()
        user, _, _ = self.create_test_data(db)
        db.close()

        response = client.get(f"/bookmarks/users/{user.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["bookmarks"]) == 0
        assert data["total"] == 0
        assert data["has_more"] == False

    def test_get_user_bookmarks_nonexistent_user(self, client: TestClient, test_db):
        """Test getting bookmarks for user that doesn't exist."""
        response = client.get("/bookmarks/users/99999")
        assert response.status_code == 404
        data = response.json()
        assert "user not found" in data["detail"].lower()

    def test_bookmarks_pagination(self, client: TestClient, test_db):
        """Test pagination for user bookmarks."""
        db = test_db()
        user, _, _ = self.create_test_data(db)
        
        # Create multiple posts and bookmarks
        posts = []
        for i in range(5):
            post = BlogPost(
                title=f"Test Post {i+1}",
                content=f"Content for test post {i+1}",
                slug=f"test-post-{i+1}",
                author_id=user.id
            )
            db.add(post)
            posts.append(post)
        
        db.commit()
        for post in posts:
            db.refresh(post)
            bookmark = Bookmark(user_id=user.id, post_id=post.id)
            db.add(bookmark)
        db.commit()
        db.close()

        # Test first page
        response = client.get(f"/bookmarks/users/{user.id}?limit=2&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data["bookmarks"]) == 2
        assert data["total"] == 5
        assert data["has_more"] == True

        # Test second page
        response = client.get(f"/bookmarks/users/{user.id}?limit=2&offset=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["bookmarks"]) == 2
        assert data["offset"] == 2

    def test_check_bookmark_status_bookmarked(self, client: TestClient, test_db):
        """Test checking bookmark status for a bookmarked post."""
        db = test_db()
        user, post1, _ = self.create_test_data(db)
        
        # Create bookmark
        bookmark = Bookmark(user_id=user.id, post_id=post1.id)
        db.add(bookmark)
        db.commit()
        db.close()

        # Check bookmark status
        response = client.get(f"/bookmarks/posts/{post1.id}/status?user_id={user.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["is_bookmarked"] == True
        assert data["user_id"] == user.id
        assert data["post_id"] == post1.id

    def test_check_bookmark_status_not_bookmarked(self, client: TestClient, test_db):
        """Test checking bookmark status for a non-bookmarked post."""
        db = test_db()
        user, post1, _ = self.create_test_data(db)
        db.close()

        # Check bookmark status
        response = client.get(f"/bookmarks/posts/{post1.id}/status?user_id={user.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["is_bookmarked"] == False
        assert data["user_id"] == user.id
        assert data["post_id"] == post1.id

    def test_get_bookmark_statistics(self, client: TestClient, test_db):
        """Test getting bookmark statistics for a user."""
        db = test_db()
        user, post1, post2 = self.create_test_data(db)
        
        # Create some bookmarks
        bookmark1 = Bookmark(user_id=user.id, post_id=post1.id)
        bookmark2 = Bookmark(user_id=user.id, post_id=post2.id)
        db.add(bookmark1)
        db.add(bookmark2)
        db.commit()
        db.close()

        # Get bookmark statistics
        response = client.get(f"/bookmarks/users/{user.id}/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_bookmarks"] == 2
        assert data["user_id"] == user.id

    def test_get_recent_bookmarks(self, client: TestClient, test_db):
        """Test getting recent bookmarks for a user."""
        db = test_db()
        user, post1, post2 = self.create_test_data(db)
        
        # Create bookmarks
        bookmark1 = Bookmark(user_id=user.id, post_id=post1.id)
        bookmark2 = Bookmark(user_id=user.id, post_id=post2.id)
        db.add(bookmark1)
        db.add(bookmark2)
        db.commit()
        db.close()

        # Get recent bookmarks (default limit should be 5)
        response = client.get(f"/bookmarks/users/{user.id}/recent")
        assert response.status_code == 200
        data = response.json()
        assert len(data["bookmarks"]) == 2
        
        # Should be ordered by created_at (most recent first)
        # Since we created bookmark2 after bookmark1, it should come first
        assert data["bookmarks"][0]["post"]["title"] == "Web Development with FastAPI"
        assert data["bookmarks"][1]["post"]["title"] == "How to Learn Python"

    def test_get_recent_bookmarks_with_limit(self, client: TestClient, test_db):
        """Test getting recent bookmarks with custom limit."""
        db = test_db()
        user, _, _ = self.create_test_data(db)
        
        # Create multiple posts and bookmarks
        for i in range(3):
            post = BlogPost(
                title=f"Recent Post {i+1}",
                content=f"Content for recent post {i+1}",
                slug=f"recent-post-{i+1}",
                author_id=user.id
            )
            db.add(post)
            db.commit()
            db.refresh(post)
            
            bookmark = Bookmark(user_id=user.id, post_id=post.id)
            db.add(bookmark)
            db.commit()
        db.close()

        # Get recent bookmarks with limit of 2
        response = client.get(f"/bookmarks/users/{user.id}/recent?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["bookmarks"]) == 2