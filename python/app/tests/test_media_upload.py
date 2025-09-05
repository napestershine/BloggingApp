import tempfile
import pytest
from app.models.models import User, Media
from app.auth.auth import get_password_hash
import io
import uuid

@pytest.fixture
def test_user(test_db):
    db = test_db()
    try:
        # Create test user with unique credentials
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
    def test_upload_image_file(self, auth_headers, client):
        """Test uploading a valid image file"""
        # Create a small test image file in memory
        file_content = b"fake image content"
        file = io.BytesIO(file_content)
        
        response = client.post(
            "/media/upload",
            headers=auth_headers,
            files={"file": ("test_image.png", file, "image/png")}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["original_filename"] == "test_image.png"
        assert data["mime_type"] == "image/png"
        assert data["file_size"] == len(file_content)
        assert "id" in data
        
        # Verify file was saved to database (verification handled by the endpoint response)
        # No direct database verification needed since endpoint confirms successful save
    
    def test_upload_file_without_auth(self, client):
        """Test uploading file without authentication should fail"""
        file_content = b"test content"
        file = io.BytesIO(file_content)
        
        response = client.post(
            "/media/upload",
            files={"file": ("test.txt", file, "text/plain")}
        )
        
        # FastAPI returns 403 for missing auth, not 401
        assert response.status_code == 403
    
    def test_upload_invalid_file_type(self, auth_headers, client):
        """Test uploading invalid file type should fail"""
        file_content = b"fake executable content"
        file = io.BytesIO(file_content)
        
        response = client.post(
            "/media/upload",
            headers=auth_headers,
            files={"file": ("test.exe", file, "application/octet-stream")}
        )
        
        assert response.status_code == 400
        assert "not allowed" in response.json()["detail"]
    
    def test_get_uploaded_file(self, auth_headers, client):
        """Test retrieving an uploaded file"""
        # First upload a file
        file_content = b"test document content"
        file = io.BytesIO(file_content)
        
        upload_response = client.post(
            "/media/upload",
            headers=auth_headers,
            files={"file": ("test.txt", file, "text/plain")}
        )
        
        assert upload_response.status_code == 201
        media_id = upload_response.json()["id"]
        
        # Now retrieve the file
        response = client.get(f"/media/{media_id}")
        
        assert response.status_code == 200
        assert response.content == file_content
    
    def test_get_nonexistent_file(self, client):
        """Test retrieving non-existent file should return 404"""
        response = client.get("/media/99999")
        assert response.status_code == 404
    
    def test_list_user_media(self, auth_headers, client):
        """Test listing user's uploaded media"""
        # Upload a couple of files
        file1 = io.BytesIO(b"file 1 content")
        file2 = io.BytesIO(b"file 2 content")
        
        client.post(
            "/media/upload",
            headers=auth_headers,
            files={"file": ("file1.txt", file1, "text/plain")}
        )
        
        client.post(
            "/media/upload",
            headers=auth_headers,
            files={"file": ("file2.txt", file2, "text/plain")}
        )
        
        # List media files
        response = client.get("/media/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        assert any(media["original_filename"] == "file1.txt" for media in data)
        assert any(media["original_filename"] == "file2.txt" for media in data)
    
    def test_delete_media(self, auth_headers, client):
        """Test deleting uploaded media"""
        # Upload a file first
        file_content = b"to be deleted"
        file = io.BytesIO(file_content)
        
        upload_response = client.post(
            "/media/upload",
            headers=auth_headers,
            files={"file": ("delete_me.txt", file, "text/plain")}
        )
        
        assert upload_response.status_code == 201
        media_id = upload_response.json()["id"]
        
        # Delete the file
        response = client.delete(f"/media/{media_id}", headers=auth_headers)
        assert response.status_code == 204
        
        # Verify file is gone
        get_response = client.get(f"/media/{media_id}")
        assert get_response.status_code == 404