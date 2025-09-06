"""
Test for the improved API code
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.security import SecurityValidator
from app.schemas.responses import HealthCheckResponse

client = TestClient(app)

def test_app_startup():
    """Test that the application starts correctly"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to the Blog API"
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"

def test_enhanced_health_check():
    """Test the enhanced health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    
    # Validate response structure
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data
    assert "uptime" in data
    assert "database" in data
    assert "dependencies" in data

def test_error_handling_404():
    """Test error handling for non-existent endpoints"""
    response = client.get("/non-existent-endpoint")
    assert response.status_code == 404
    
    # FastAPI default 404 response format
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not Found"

def test_security_validator_email():
    """Test email validation utility"""
    # Valid emails
    assert SecurityValidator.validate_email("test@example.com") is True
    assert SecurityValidator.validate_email("user.name+tag@domain.co.uk") is True
    
    # Invalid emails
    assert SecurityValidator.validate_email("invalid-email") is False
    assert SecurityValidator.validate_email("@domain.com") is False
    assert SecurityValidator.validate_email("user@") is False
    assert SecurityValidator.validate_email("") is False

def test_security_validator_username():
    """Test username validation utility"""
    # Valid usernames
    assert SecurityValidator.validate_username("validuser") is True
    assert SecurityValidator.validate_username("user123") is True
    assert SecurityValidator.validate_username("user_name") is True
    
    # Invalid usernames
    assert SecurityValidator.validate_username("ab") is False  # Too short
    assert SecurityValidator.validate_username("user-name") is False  # Invalid character
    assert SecurityValidator.validate_username("user name") is False  # Space
    assert SecurityValidator.validate_username("") is False

def test_security_validator_password_strength():
    """Test password strength validation"""
    # Strong password
    result = SecurityValidator.validate_password_strength("StrongP@ssw0rd!")
    assert result["valid"] is True
    
    # Weak passwords
    weak_result = SecurityValidator.validate_password_strength("123")
    assert weak_result["valid"] is False
    assert "must be at least 8 characters" in weak_result["message"]
    
    no_upper_result = SecurityValidator.validate_password_strength("password123!")
    assert no_upper_result["valid"] is False
    assert "uppercase letter" in no_upper_result["message"]

def test_security_validator_sanitize_input():
    """Test input sanitization"""
    # Safe input
    safe_input = "This is safe content"
    assert SecurityValidator.sanitize_input(safe_input) == safe_input
    
    # HTML escaping
    html_input = "<p>Hello World</p>"
    sanitized = SecurityValidator.sanitize_input(html_input)
    assert "&lt;p&gt;" in sanitized
    assert "&lt;/p&gt;" in sanitized

def test_cors_headers():
    """Test CORS headers are present but restrictive"""
    response = client.options("/")
    
    # Should not allow all origins (security improvement)
    cors_header = response.headers.get("access-control-allow-origin")
    if cors_header:
        assert cors_header != "*"  # Should be more restrictive

def test_request_logging_header():
    """Test that process time header is added"""
    response = client.get("/")
    assert "X-Process-Time" in response.headers
    
    # Should be a valid float
    process_time = float(response.headers["X-Process-Time"])
    assert process_time >= 0

if __name__ == "__main__":
    pytest.main([__file__])