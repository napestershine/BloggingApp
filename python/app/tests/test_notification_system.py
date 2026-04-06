from fastapi.testclient import TestClient

from app.auth.auth import get_current_user
from app.main import app
from app.models.models import Notification, NotificationType, User


def _create_notification(db, user_id, notif_type=NotificationType.FOLLOW, **overrides):
    notification = Notification(
        user_id=user_id,
        type=notif_type,
        title=overrides.pop("title", "Test notification"),
        message=overrides.pop("message", "Test message"),
        **overrides,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


class TestNotificationSystemEndpoints:
    def setup_method(self):
        app.dependency_overrides.pop(get_current_user, None)

    def teardown_method(self):
        app.dependency_overrides.pop(get_current_user, None)

    def _setup_authenticated_user(self, test_db):
        db = test_db()
        user = User(
            username="notif_user",
            email="notif_user@example.com",
            name="Notification User",
            hashed_password="hashed",
        )
        other_user = User(
            username="notif_other",
            email="notif_other@example.com",
            name="Other User",
            hashed_password="hashed",
        )
        db.add_all([user, other_user])
        db.commit()
        db.refresh(user)
        db.refresh(other_user)

        def override_get_current_user():
            return db.get(User, user.id)

        app.dependency_overrides[get_current_user] = override_get_current_user
        return db, user, other_user

    def test_get_notifications_returns_only_current_user_notifications(self, client: TestClient, test_db):
        db, user, other_user = self._setup_authenticated_user(test_db)

        first = _create_notification(db, user.id, title="First")
        second = _create_notification(db, user.id, notif_type=NotificationType.POST_LIKE, title="Second")
        _create_notification(db, other_user.id, title="Other user")

        response = client.get("/notifications/?limit=10")

        assert response.status_code == 200
        data = response.json()
        returned_ids = {item["id"] for item in data}
        assert returned_ids == {first.id, second.id}
        assert {item["user_id"] for item in data} == {user.id}

    def test_get_notifications_supports_unread_only_and_type_filter(self, client: TestClient, test_db):
        db, user, _ = self._setup_authenticated_user(test_db)

        _create_notification(db, user.id, notif_type=NotificationType.FOLLOW, title="Unread follow", is_read=False)
        _create_notification(db, user.id, notif_type=NotificationType.FOLLOW, title="Read follow", is_read=True)
        _create_notification(db, user.id, notif_type=NotificationType.POST_LIKE, title="Unread like", is_read=False)

        unread_response = client.get("/notifications/?unread_only=true")
        assert unread_response.status_code == 200
        unread_titles = {item["title"] for item in unread_response.json()}
        assert unread_titles == {"Unread follow", "Unread like"}

        follow_response = client.get("/notifications/?type_filter=follow")
        assert follow_response.status_code == 200
        follow_titles = {item["title"] for item in follow_response.json()}
        assert follow_titles == {"Unread follow", "Read follow"}

    def test_get_notification_stats_returns_total_and_unread_counts(self, client: TestClient, test_db):
        db, user, _ = self._setup_authenticated_user(test_db)

        _create_notification(db, user.id, title="Unread one", is_read=False)
        _create_notification(db, user.id, title="Unread two", is_read=False)
        _create_notification(db, user.id, title="Read one", is_read=True)

        response = client.get("/notifications/stats")

        assert response.status_code == 200
        assert response.json() == {"total_count": 3, "unread_count": 2}

    def test_update_notification_marks_item_as_read(self, client: TestClient, test_db):
        db, user, _ = self._setup_authenticated_user(test_db)
        notification = _create_notification(db, user.id, is_read=False)

        response = client.put(
            f"/notifications/{notification.id}",
            json={"is_read": True},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == notification.id
        assert data["is_read"] is True
        assert data["read_at"] is not None

    def test_mark_all_notifications_read_only_updates_current_user(self, client: TestClient, test_db):
        db, user, other_user = self._setup_authenticated_user(test_db)

        _create_notification(db, user.id, title="User unread 1", is_read=False)
        _create_notification(db, user.id, title="User unread 2", is_read=False)
        _create_notification(db, other_user.id, title="Other unread", is_read=False)

        response = client.patch("/notifications/read-all")

        assert response.status_code == 200
        assert response.json()["count"] == 2
        assert db.query(Notification).filter_by(user_id=user.id, is_read=False).count() == 0
        assert db.query(Notification).filter_by(user_id=other_user.id, is_read=False).count() == 1

    def test_delete_notification_is_scoped_to_current_user(self, client: TestClient, test_db):
        db, user, other_user = self._setup_authenticated_user(test_db)
        own_notification = _create_notification(db, user.id, title="Own notification")
        other_notification = _create_notification(db, other_user.id, title="Other notification")

        other_response = client.delete(f"/notifications/{other_notification.id}")
        assert other_response.status_code == 404

        own_response = client.delete(f"/notifications/{own_notification.id}")
        assert own_response.status_code == 200
        assert own_response.json()["message"] == "Notification deleted successfully"
        assert db.query(Notification).filter_by(id=own_notification.id).count() == 0

    def test_delete_all_notifications_respects_limit_and_read_only(self, client: TestClient, test_db):
        db, user, other_user = self._setup_authenticated_user(test_db)

        for index in range(3):
            _create_notification(
                db,
                user.id,
                title=f"Read {index}",
                is_read=True,
            )
        for index in range(2):
            _create_notification(
                db,
                user.id,
                notif_type=NotificationType.POST_LIKE,
                title=f"Unread {index}",
                is_read=False,
            )
        _create_notification(db, other_user.id, title="Other read", is_read=True)

        response = client.delete("/notifications/?read_only=true&limit=2")

        assert response.status_code == 200
        assert response.json()["count"] == 2
        assert db.query(Notification).filter_by(user_id=user.id).count() == 3
        assert db.query(Notification).filter_by(user_id=user.id, is_read=True).count() == 1
        assert db.query(Notification).filter_by(user_id=other_user.id).count() == 1
