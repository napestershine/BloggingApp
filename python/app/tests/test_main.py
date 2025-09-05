import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Blog API"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "name": "Test User",
            "password": "TestPass123",
            "retyped_password": "TestPass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data

def test_register_user_password_mismatch():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser2",
            "email": "test2@example.com", 
            "name": "Test User 2",
            "password": "TestPass123",
            "retyped_password": "DifferentPass123"
        }
    )
    assert response.status_code == 400
    assert "Passwords do not match" in response.json()["detail"]