import pytest
from app.models.models import User, Media, MediaType
from app.auth.auth import get_password_hash
import uuid

@pytest.fixture
def test_user(test_db):
    db = test_db()
    try:
        unique_id = str(uuid.uuid4())[:8]
        user = User(
            username=f"testuser_{unique_id}",
            email=f"test_{unique_id}@example.com",
            name="Test User",
            hashed_password=get_password_hash("testpass123")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

@pytest.fixture
def auth_headers(test_user, client):
    login_data = {
        "username": test_user.username,
        "password": "testpass123"
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

class TestMediaUpload:
    def test_upload_image(self, auth_headers, client):
        """Test uploading an image file"""
        # Create a mock image file
        files = {"file": ("test.jpg", b"fake image data", "image/jpeg")}
        
        response = client.post("/media/upload", files=files, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["filename"] == "test.jpg"
        assert data["media_type"] == "IMAGE"
        assert "url" in data
        assert "id" in data

    def test_upload_video(self, auth_headers, client):
        """Test uploading a video file"""
        files = {"file": ("test.mp4", b"fake video data", "video/mp4")}
        
        response = client.post("/media/upload", files=files, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["filename"] == "test.mp4"
        assert data["media_type"] == "VIDEO"

    def test_upload_document(self, auth_headers, client):
        """Test uploading a document file"""
        files = {"file": ("test.pdf", b"fake pdf data", "application/pdf")}
        
        response = client.post("/media/upload", files=files, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["filename"] == "test.pdf"
        assert data["media_type"] == "DOCUMENT"

    def test_upload_without_auth(self, client):
        """Test that upload requires authentication"""
        files = {"file": ("test.jpg", b"fake image data", "image/jpeg")}
        
        response = client.post("/media/upload", files=files)
        
        assert response.status_code == 401

    def test_get_user_media(self, auth_headers, client):
        """Test getting user's uploaded media"""
        # First upload a file
        files = {"file": ("test.jpg", b"fake image data", "image/jpeg")}
        client.post("/media/upload", files=files, headers=auth_headers)
        
        # Then get user's media
        response = client.get("/media/user", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["filename"] == "test.jpg"

    def test_get_media_by_id(self, auth_headers, client):
        """Test getting specific media by ID"""
        # First upload a file
        files = {"file": ("test.jpg", b"fake image data", "image/jpeg")}
        upload_response = client.post("/media/upload", files=files, headers=auth_headers)
        media_id = upload_response.json()["id"]
        
        # Then get the media by ID
        response = client.get(f"/media/{media_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == media_id
        assert data["filename"] == "test.jpg"

    def test_delete_media(self, auth_headers, client):
        """Test deleting uploaded media"""
        # First upload a file
        files = {"file": ("test.jpg", b"fake image data", "image/jpeg")}
        upload_response = client.post("/media/upload", files=files, headers=auth_headers)
        media_id = upload_response.json()["id"]
        
        # Then delete the media
        response = client.delete(f"/media/{media_id}", headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Media deleted successfully"
        
        # Verify it's deleted
        get_response = client.get(f"/media/{media_id}", headers=auth_headers)
        assert get_response.status_code == 404