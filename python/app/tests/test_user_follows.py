import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.models import User, UserFollow


class TestUserFollowEndpoints:
    """Test suite for user follow functionality."""

    def create_test_users(self, db):
        """Helper to create test users."""
        user1 = User(
            username="alice",
            email="alice@example.com",
            name="Alice Smith",
            hashed_password="hashed"
        )
        user2 = User(
            username="bob", 
            email="bob@example.com",
            name="Bob Johnson",
            hashed_password="hashed"
        )
        db.add(user1)
        db.add(user2)
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        return user1, user2

    def test_follow_user_success(self, client: TestClient, test_db):
        """Test successfully following a user."""
        db = test_db()
        user1, user2 = self.create_test_users(db)
        db.close()

        # Follow user2 as user1
        response = client.post(f"/follow/users/{user2.id}", json={"follower_id": user1.id})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Successfully followed {user2.username}"
        assert data["follower_id"] == user1.id
        assert data["following_id"] == user2.id

    def test_follow_user_already_following(self, client: TestClient, test_db):
        """Test following a user that's already followed."""
        db = test_db()
        user1, user2 = self.create_test_users(db)
        
        # Create existing follow relationship
        follow = UserFollow(follower_id=user1.id, following_id=user2.id)
        db.add(follow)
        db.commit()
        db.close()

        # Try to follow again
        response = client.post(f"/follow/users/{user2.id}", json={"follower_id": user1.id})
        assert response.status_code == 400
        data = response.json()
        assert "already following" in data["detail"].lower()

    def test_follow_self_error(self, client: TestClient, test_db):
        """Test that users cannot follow themselves."""
        db = test_db()
        user1, _ = self.create_test_users(db)
        db.close()

        # Try to follow self
        response = client.post(f"/follow/users/{user1.id}", json={"follower_id": user1.id})
        assert response.status_code == 400
        data = response.json()
        assert "cannot follow yourself" in data["detail"].lower()

    def test_follow_nonexistent_user(self, client: TestClient, test_db):
        """Test following a user that doesn't exist."""
        db = test_db()
        user1, _ = self.create_test_users(db)
        db.close()

        # Try to follow non-existent user
        response = client.post("/follow/users/99999", json={"follower_id": user1.id})
        assert response.status_code == 404
        data = response.json()
        assert "user not found" in data["detail"].lower()

    def test_unfollow_user_success(self, client: TestClient, test_db):
        """Test successfully unfollowing a user."""
        db = test_db()
        user1, user2 = self.create_test_users(db)
        
        # Create follow relationship
        follow = UserFollow(follower_id=user1.id, following_id=user2.id)
        db.add(follow)
        db.commit()
        db.close()

        # Unfollow user2 as user1
        response = client.delete(f"/follow/users/{user2.id}?follower_id={user1.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Successfully unfollowed {user2.username}"

    def test_unfollow_user_not_following(self, client: TestClient, test_db):
        """Test unfollowing a user that's not being followed."""
        db = test_db()
        user1, user2 = self.create_test_users(db)
        db.close()

        # Try to unfollow without following first
        response = client.delete(f"/follow/users/{user2.id}?follower_id={user1.id}")
        assert response.status_code == 400
        data = response.json()
        assert "not following" in data["detail"].lower()

    def test_get_user_followers(self, client: TestClient, test_db):
        """Test getting a user's followers list."""
        db = test_db()
        user1, user2 = self.create_test_users(db)
        
        # Create additional user to follow user2
        user3 = User(
            username="charlie",
            email="charlie@example.com",
            name="Charlie Brown",
            hashed_password="hashed"
        )
        db.add(user3)
        db.commit()
        db.refresh(user3)

        # Both user1 and user3 follow user2
        follow1 = UserFollow(follower_id=user1.id, following_id=user2.id)
        follow2 = UserFollow(follower_id=user3.id, following_id=user2.id)
        db.add(follow1)
        db.add(follow2)
        db.commit()
        db.close()

        # Get user2's followers
        response = client.get(f"/follow/users/{user2.id}/followers")
        assert response.status_code == 200
        data = response.json()
        assert len(data["followers"]) == 2
        assert data["total"] == 2
        
        usernames = [follower["username"] for follower in data["followers"]]
        assert "alice" in usernames
        assert "charlie" in usernames

    def test_get_user_following(self, client: TestClient, test_db):
        """Test getting a user's following list."""
        db = test_db()
        user1, user2 = self.create_test_users(db)
        
        # Create additional user for user1 to follow
        user3 = User(
            username="dave",
            email="dave@example.com",
            name="Dave Wilson",
            hashed_password="hashed"
        )
        db.add(user3)
        db.commit()
        db.refresh(user3)

        # User1 follows both user2 and user3
        follow1 = UserFollow(follower_id=user1.id, following_id=user2.id)
        follow2 = UserFollow(follower_id=user1.id, following_id=user3.id)
        db.add(follow1)
        db.add(follow2)
        db.commit()
        db.close()

        # Get user1's following list
        response = client.get(f"/follow/users/{user1.id}/following")
        assert response.status_code == 200
        data = response.json()
        assert len(data["following"]) == 2
        assert data["total"] == 2
        
        usernames = [following["username"] for following in data["following"]]
        assert "bob" in usernames
        assert "dave" in usernames

    def test_get_follow_stats(self, client: TestClient, test_db):
        """Test getting user follow statistics."""
        db = test_db()
        user1, user2 = self.create_test_users(db)
        
        # Create additional users
        user3 = User(username="charlie", email="charlie@example.com", name="Charlie", hashed_password="hashed")
        user4 = User(username="dave", email="dave@example.com", name="Dave", hashed_password="hashed")
        db.add(user3)
        db.add(user4)
        db.commit()
        db.refresh(user3)
        db.refresh(user4)

        # User1 follows user2 and user3
        # User3 and user4 follow user1
        follows = [
            UserFollow(follower_id=user1.id, following_id=user2.id),
            UserFollow(follower_id=user1.id, following_id=user3.id),
            UserFollow(follower_id=user3.id, following_id=user1.id),
            UserFollow(follower_id=user4.id, following_id=user1.id)
        ]
        for follow in follows:
            db.add(follow)
        db.commit()
        db.close()

        # Get user1's follow stats
        response = client.get(f"/follow/users/{user1.id}/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["followers_count"] == 2
        assert data["following_count"] == 2
        assert data["user_id"] == user1.id

    def test_followers_pagination(self, client: TestClient, test_db):
        """Test pagination for followers list."""
        db = test_db()
        user1, user2 = self.create_test_users(db)
        
        # Create multiple followers
        followers = []
        for i in range(5):
            user = User(
                username=f"follower{i}",
                email=f"follower{i}@example.com",
                name=f"Follower {i}",
                hashed_password="hashed"
            )
            db.add(user)
            followers.append(user)
        
        db.commit()
        for follower in followers:
            db.refresh(follower)
            follow = UserFollow(follower_id=follower.id, following_id=user1.id)
            db.add(follow)
        db.commit()
        db.close()

        # Test first page
        response = client.get(f"/follow/users/{user1.id}/followers?limit=2&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data["followers"]) == 2
        assert data["total"] == 5
        assert data["has_more"] == True

        # Test second page
        response = client.get(f"/follow/users/{user1.id}/followers?limit=2&offset=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["followers"]) == 2
        assert data["offset"] == 2

    def test_following_pagination(self, client: TestClient, test_db):
        """Test pagination for following list."""
        db = test_db()
        user1, user2 = self.create_test_users(db)
        
        # Create multiple users to follow
        following_users = []
        for i in range(5):
            user = User(
                username=f"user{i}",
                email=f"user{i}@example.com",
                name=f"User {i}",
                hashed_password="hashed"
            )
            db.add(user)
            following_users.append(user)
        
        db.commit()
        for followed_user in following_users:
            db.refresh(followed_user)
            follow = UserFollow(follower_id=user1.id, following_id=followed_user.id)
            db.add(follow)
        db.commit()
        db.close()

        # Test first page
        response = client.get(f"/follow/users/{user1.id}/following?limit=3&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data["following"]) == 3
        assert data["total"] == 5
        assert data["has_more"] == True

    def test_get_followers_empty_list(self, client: TestClient, test_db):
        """Test getting followers for user with no followers."""
        db = test_db()
        user1, _ = self.create_test_users(db)
        db.close()

        response = client.get(f"/follow/users/{user1.id}/followers")
        assert response.status_code == 200
        data = response.json()
        assert len(data["followers"]) == 0
        assert data["total"] == 0
        assert data["has_more"] == False

    def test_get_following_empty_list(self, client: TestClient, test_db):
        """Test getting following for user who follows no one."""
        db = test_db()
        user1, _ = self.create_test_users(db)
        db.close()

        response = client.get(f"/follow/users/{user1.id}/following")
        assert response.status_code == 200
        data = response.json()
        assert len(data["following"]) == 0
        assert data["total"] == 0
        assert data["has_more"] == False