import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.models import User, BlogPost, Notification, NotificationType


class TestNotificationSystemEndpoints:
    """Test suite for the enhanced notification system."""

    def create_test_data(self, db):
        """Helper to create test users and posts."""
        user1 = User(
            username="testuser1",
            email="test1@example.com",
            name="Test User 1",
            hashed_password="hashed"
        )
        user2 = User(
            username="testuser2",
            email="test2@example.com",
            name="Test User 2",
            hashed_password="hashed"
        )
        db.add(user1)
        db.add(user2)
        db.commit()
        db.refresh(user1)
        db.refresh(user2)

        post = BlogPost(
            title="Test Blog Post",
            content="This is a test blog post for notifications",
            slug="test-blog-post",
            author_id=user1.id
        )
        db.add(post)
        db.commit()
        db.refresh(post)
        
        return user1, user2, post

    def test_create_notification_success(self, client: TestClient, test_db):
        """Test creating a notification successfully."""
        db = test_db()
        user1, user2, post = self.create_test_data(db)
        db.close()

        # Create a follow notification
        notification_data = {
            "user_id": user1.id,
            "type": "follow",
            "title": "New Follower",
            "message": f"{user2.username} started following you",
            "related_user_id": user2.id
        }

        response = client.post("/notifications/", json=notification_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Follower"
        assert data["type"] == "follow"
        assert data["is_read"] == False
        assert data["user_id"] == user1.id
        assert data["related_user_id"] == user2.id

    def test_create_notification_invalid_type(self, client: TestClient, test_db):
        """Test creating notification with invalid type."""
        db = test_db()
        user1, user2, _ = self.create_test_data(db)
        db.close()

        notification_data = {
            "user_id": user1.id,
            "type": "invalid_type",
            "title": "Test Notification",
            "message": "Test message"
        }

        response = client.post("/notifications/", json=notification_data)
        assert response.status_code == 422  # Validation error

    def test_get_user_notifications(self, client: TestClient, test_db):
        """Test getting notifications for a user."""
        db = test_db()
        user1, user2, post = self.create_test_data(db)
        
        # Create multiple notifications
        notifications = [
            Notification(
                user_id=user1.id,
                type=NotificationType.FOLLOW,
                title="New Follower",
                message=f"{user2.username} started following you",
                related_user_id=user2.id
            ),
            Notification(
                user_id=user1.id,
                type=NotificationType.POST_LIKE,
                title="Post Liked",
                message=f"{user2.username} liked your post",
                related_user_id=user2.id,
                related_post_id=post.id
            )
        ]
        
        for notification in notifications:
            db.add(notification)
        db.commit()
        db.close()

        # Get user notifications
        response = client.get(f"/notifications/users/{user1.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["notifications"]) == 2
        assert data["total"] == 2
        
        # Check notification types
        types = [notif["type"] for notif in data["notifications"]]
        assert "follow" in types
        assert "post_like" in types

    def test_get_user_notifications_empty(self, client: TestClient, test_db):
        """Test getting notifications for user with no notifications."""
        db = test_db()
        user1, _, _ = self.create_test_data(db)
        db.close()

        response = client.get(f"/notifications/users/{user1.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["notifications"]) == 0
        assert data["total"] == 0
        assert data["has_more"] == False

    def test_get_user_notifications_nonexistent_user(self, client: TestClient, test_db):
        """Test getting notifications for user that doesn't exist."""
        response = client.get("/notifications/users/99999")
        assert response.status_code == 404
        data = response.json()
        assert "user not found" in data["detail"].lower()

    def test_mark_notification_as_read(self, client: TestClient, test_db):
        """Test marking a notification as read."""
        db = test_db()
        user1, user2, _ = self.create_test_data(db)
        
        # Create notification
        notification = Notification(
            user_id=user1.id,
            type=NotificationType.FOLLOW,
            title="New Follower",
            message=f"{user2.username} started following you",
            related_user_id=user2.id,
            is_read=False
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        db.close()

        # Mark as read
        response = client.patch(f"/notifications/{notification.id}/read")
        assert response.status_code == 200
        data = response.json()
        assert data["is_read"] == True
        assert data["read_at"] is not None

    def test_mark_notification_as_unread(self, client: TestClient, test_db):
        """Test marking a notification as unread."""
        db = test_db()
        user1, user2, _ = self.create_test_data(db)
        
        # Create read notification
        notification = Notification(
            user_id=user1.id,
            type=NotificationType.FOLLOW,
            title="New Follower",
            message=f"{user2.username} started following you",
            related_user_id=user2.id,
            is_read=True
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        db.close()

        # Mark as unread
        response = client.patch(f"/notifications/{notification.id}/unread")
        assert response.status_code == 200
        data = response.json()
        assert data["is_read"] == False
        assert data["read_at"] is None

    def test_delete_notification(self, client: TestClient, test_db):
        """Test deleting a notification."""
        db = test_db()
        user1, user2, _ = self.create_test_data(db)
        
        # Create notification
        notification = Notification(
            user_id=user1.id,
            type=NotificationType.FOLLOW,
            title="New Follower",
            message=f"{user2.username} started following you",
            related_user_id=user2.id
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        db.close()

        # Delete notification
        response = client.delete(f"/notifications/{notification.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Notification deleted successfully"

    def test_delete_nonexistent_notification(self, client: TestClient, test_db):
        """Test deleting a notification that doesn't exist."""
        response = client.delete("/notifications/99999")
        assert response.status_code == 404
        data = response.json()
        assert "notification not found" in data["detail"].lower()

    def test_get_notification_statistics(self, client: TestClient, test_db):
        """Test getting notification statistics for a user."""
        db = test_db()
        user1, user2, post = self.create_test_data(db)
        
        # Create notifications with different read statuses
        notifications = [
            Notification(user_id=user1.id, type=NotificationType.FOLLOW, title="Test 1", message="Test", is_read=False),
            Notification(user_id=user1.id, type=NotificationType.POST_LIKE, title="Test 2", message="Test", is_read=False),
            Notification(user_id=user1.id, type=NotificationType.POST_COMMENT, title="Test 3", message="Test", is_read=True)
        ]
        
        for notification in notifications:
            db.add(notification)
        db.commit()
        db.close()

        # Get notification statistics
        response = client.get(f"/notifications/users/{user1.id}/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_notifications"] == 3
        assert data["unread_count"] == 2
        assert data["read_count"] == 1
        assert data["user_id"] == user1.id

    def test_mark_all_notifications_as_read(self, client: TestClient, test_db):
        """Test marking all notifications as read for a user."""
        db = test_db()
        user1, user2, _ = self.create_test_data(db)
        
        # Create multiple unread notifications
        notifications = [
            Notification(user_id=user1.id, type=NotificationType.FOLLOW, title="Test 1", message="Test", is_read=False),
            Notification(user_id=user1.id, type=NotificationType.POST_LIKE, title="Test 2", message="Test", is_read=False),
            Notification(user_id=user1.id, type=NotificationType.POST_COMMENT, title="Test 3", message="Test", is_read=False)
        ]
        
        for notification in notifications:
            db.add(notification)
        db.commit()
        db.close()

        # Mark all as read
        response = client.patch(f"/notifications/users/{user1.id}/mark-all-read")
        assert response.status_code == 200
        data = response.json()
        assert data["marked_count"] == 3
        assert data["message"] == "All notifications marked as read"

    def test_notifications_pagination(self, client: TestClient, test_db):
        """Test pagination for user notifications."""
        db = test_db()
        user1, user2, _ = self.create_test_data(db)
        
        # Create multiple notifications
        for i in range(5):
            notification = Notification(
                user_id=user1.id,
                type=NotificationType.FOLLOW,
                title=f"Test Notification {i+1}",
                message=f"Test message {i+1}",
                related_user_id=user2.id
            )
            db.add(notification)
        db.commit()
        db.close()

        # Test first page
        response = client.get(f"/notifications/users/{user1.id}?limit=2&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data["notifications"]) == 2
        assert data["total"] == 5
        assert data["has_more"] == True

        # Test second page
        response = client.get(f"/notifications/users/{user1.id}?limit=2&offset=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["notifications"]) == 2
        assert data["offset"] == 2

    def test_filter_notifications_by_type(self, client: TestClient, test_db):
        """Test filtering notifications by type."""
        db = test_db()
        user1, user2, post = self.create_test_data(db)
        
        # Create notifications of different types
        notifications = [
            Notification(user_id=user1.id, type=NotificationType.FOLLOW, title="Follow", message="Follow msg"),
            Notification(user_id=user1.id, type=NotificationType.POST_LIKE, title="Like", message="Like msg"),
            Notification(user_id=user1.id, type=NotificationType.POST_COMMENT, title="Comment", message="Comment msg")
        ]
        
        for notification in notifications:
            db.add(notification)
        db.commit()
        db.close()

        # Filter by follow type
        response = client.get(f"/notifications/users/{user1.id}?type=follow")
        assert response.status_code == 200
        data = response.json()
        assert len(data["notifications"]) == 1
        assert data["notifications"][0]["type"] == "follow"

    def test_filter_notifications_by_read_status(self, client: TestClient, test_db):
        """Test filtering notifications by read/unread status."""
        db = test_db()
        user1, user2, _ = self.create_test_data(db)
        
        # Create notifications with different read statuses
        notifications = [
            Notification(user_id=user1.id, type=NotificationType.FOLLOW, title="Read", message="Read msg", is_read=True),
            Notification(user_id=user1.id, type=NotificationType.POST_LIKE, title="Unread 1", message="Unread msg", is_read=False),
            Notification(user_id=user1.id, type=NotificationType.POST_COMMENT, title="Unread 2", message="Unread msg", is_read=False)
        ]
        
        for notification in notifications:
            db.add(notification)
        db.commit()
        db.close()

        # Filter unread notifications
        response = client.get(f"/notifications/users/{user1.id}?unread_only=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data["notifications"]) == 2
        for notif in data["notifications"]:
            assert notif["is_read"] == False