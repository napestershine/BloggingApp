import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.models import User
from app.auth.auth import get_current_user


class TestWhatsAppNotificationEndpoints:
    """Test WhatsApp notification endpoints"""
    
    def setup_method(self):
        """Setup for each test method"""
        # This will be called before each test method
        pass
    
    def test_get_whatsapp_settings(self, client):
        """Test getting WhatsApp settings for user"""
        # First register and login a user
        username = "testnotif1"
        email = "testnotif1@example.com"
        
        registration_data = {
            "username": username,
            "password": "testpass123",
            "retyped_password": "testpass123",
            "name": "Test Notification User",
            "email": email
        }
        
        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == 201
        
        # Login to get token
        login_data = {"username": username, "password": "testpass123"}
        response = client.post("/auth/login", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Now test the whatsapp settings endpoint
        response = client.get("/notifications/whatsapp", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["whatsapp_number"] is None
        assert data["whatsapp_notifications_enabled"] is False
        assert data["notify_on_new_posts"] is True
        assert data["notify_on_comments"] is True
        assert data["notify_on_mentions"] is True
    
    def test_update_whatsapp_settings_valid_phone(self, client):
        """Test updating WhatsApp settings with valid phone number"""
        # First register and login a user
        username = "testnotif2"
        email = "testnotif2@example.com"
        
        registration_data = {
            "username": username,
            "password": "testpass123",
            "retyped_password": "testpass123",
            "name": "Test Notification User 2",
            "email": email
        }
        
        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == 201
        
        # Login to get token
        login_data = {"username": username, "password": "testpass123"}
        response = client.post("/auth/login", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        update_data = {
            "whatsapp_number": "+1234567890",
            "whatsapp_notifications_enabled": True,
            "notify_on_new_posts": False
        }
        
        response = client.put("/notifications/whatsapp", json=update_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["whatsapp_number"] == "+1234567890"
        assert data["whatsapp_notifications_enabled"] is True
        assert data["notify_on_new_posts"] is False
    
    def test_update_whatsapp_settings_invalid_phone(self, client):
        """Test updating WhatsApp settings with invalid phone number"""
        # First register and login a user
        username = "testnotif3"
        email = "testnotif3@example.com"
        
        registration_data = {
            "username": username,
            "password": "testpass123",
            "retyped_password": "testpass123",
            "name": "Test Notification User 3",
            "email": email
        }
        
        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == 201
        
        # Login to get token
        login_data = {"username": username, "password": "testpass123"}
        response = client.post("/auth/login", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        update_data = {
            "whatsapp_number": "invalid_phone",
            "whatsapp_notifications_enabled": True
        }
        
        response = client.put("/notifications/whatsapp", json=update_data, headers=headers)
        assert response.status_code == 400
        assert "Invalid phone number format" in response.json()["detail"]
    
    def test_test_whatsapp_notification_no_phone(self, client):
        """Test sending test notification without phone number configured"""
        # First register and login a user
        username = "testnotif4"
        email = "testnotif4@example.com"
        
        registration_data = {
            "username": username,
            "password": "testpass123",
            "retyped_password": "testpass123",
            "name": "Test Notification User 4",
            "email": email
        }
        
        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == 201
        
        # Login to get token
        login_data = {"username": username, "password": "testpass123"}
        response = client.post("/auth/login", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to send test notification without phone number
        response = client.post("/notifications/whatsapp/test", headers=headers)
        assert response.status_code == 400
        assert "WhatsApp number not configured" in response.json()["detail"]
    
    def test_test_whatsapp_notification_disabled(self, client):
        """Test sending test notification when notifications are disabled"""
        # First register and login a user
        username = "testnotif5"
        email = "testnotif5@example.com"
        
        registration_data = {
            "username": username,
            "password": "testpass123",
            "retyped_password": "testpass123",
            "name": "Test Notification User 5",
            "email": email
        }
        
        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == 201
        
        # Login to get token
        login_data = {"username": username, "password": "testpass123"}
        response = client.post("/auth/login", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Set phone number but disable notifications
        update_data = {
            "whatsapp_number": "+1234567890",
            "whatsapp_notifications_enabled": False
        }
        response = client.put("/notifications/whatsapp", json=update_data, headers=headers)
        assert response.status_code == 200
        
        # Try to send test notification with notifications disabled
        response = client.post("/notifications/whatsapp/test", headers=headers)
        assert response.status_code == 400
        assert "WhatsApp notifications are disabled" in response.json()["detail"]