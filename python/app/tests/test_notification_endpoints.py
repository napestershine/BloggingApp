import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.connection import get_db, Base
from app.models.models import User
from app.auth.auth import get_current_user
from app.schemas.schemas import WhatsAppSettings

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_notifications.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Test user for authentication
def create_test_user():
    db = TestingSessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == "testuser").first()
        if existing_user:
            return existing_user
            
        test_user = User(
            username="testuser",
            email="test@example.com",
            name="Test User",
            hashed_password="fake_hash",
            whatsapp_number=None,
            whatsapp_notifications_enabled=False,
            notify_on_new_posts=True,
            notify_on_comments=True,
            notify_on_mentions=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        return test_user
    finally:
        db.close()

def override_get_current_user():
    return create_test_user()

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

class TestWhatsAppNotificationEndpoints:
    """Test WhatsApp notification endpoints"""
    
    def test_get_whatsapp_settings(self):
        """Test getting WhatsApp settings for user"""
        response = client.get("/notifications/whatsapp")
        assert response.status_code == 200
        
        data = response.json()
        assert data["whatsapp_number"] is None
        assert data["whatsapp_notifications_enabled"] is False
        assert data["notify_on_new_posts"] is True
        assert data["notify_on_comments"] is True
        assert data["notify_on_mentions"] is True
    
    def test_update_whatsapp_settings_valid_phone(self):
        """Test updating WhatsApp settings with valid phone number"""
        update_data = {
            "whatsapp_number": "+1234567890",
            "whatsapp_notifications_enabled": True,
            "notify_on_new_posts": False
        }
        
        response = client.put("/notifications/whatsapp", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["whatsapp_number"] == "+1234567890"
        assert data["whatsapp_notifications_enabled"] is True
        assert data["notify_on_new_posts"] is False
    
    def test_update_whatsapp_settings_invalid_phone(self):
        """Test updating WhatsApp settings with invalid phone number"""
        update_data = {
            "whatsapp_number": "invalid_phone",
            "whatsapp_notifications_enabled": True
        }
        
        response = client.put("/notifications/whatsapp", json=update_data)
        assert response.status_code == 400
        assert "Invalid phone number format" in response.json()["detail"]
    
    def test_test_whatsapp_notification_no_phone(self):
        """Test sending test notification without phone number configured"""
        # Create user without phone number
        user = create_test_user()
        db = TestingSessionLocal()
        try:
            user.whatsapp_number = None
            user.whatsapp_notifications_enabled = True
            db.merge(user)
            db.commit()
        finally:
            db.close()
        
        response = client.post("/notifications/whatsapp/test")
        assert response.status_code == 400
        assert "WhatsApp number not configured" in response.json()["detail"]
    
    def test_test_whatsapp_notification_disabled(self):
        """Test sending test notification when notifications are disabled"""
        # Create user with phone but notifications disabled
        user = create_test_user()
        db = TestingSessionLocal()
        try:
            user.whatsapp_number = "+1234567890"
            user.whatsapp_notifications_enabled = False
            db.merge(user)
            db.commit()
        finally:
            db.close()
        
        response = client.post("/notifications/whatsapp/test")
        assert response.status_code == 400
        assert "WhatsApp notifications are disabled" in response.json()["detail"]