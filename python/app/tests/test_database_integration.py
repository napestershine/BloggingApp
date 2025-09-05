"""Test database integration with PostgreSQL and SQLite."""
import pytest
import os
from sqlalchemy import create_engine, text


def test_database_connection_type(test_db):
    """Test that we can determine the database type being used"""
    test_database_url = os.environ.get("TEST_DATABASE_URL")
    
    if test_database_url:
        # Should be using PostgreSQL in CI
        assert "postgresql" in test_database_url.lower()
        
        # Test PostgreSQL-specific functionality
        session = test_db()
        result = session.execute(text("SELECT version()"))
        version_info = result.fetchone()[0]
        assert "PostgreSQL" in version_info
        session.close()
    else:
        # Should be using SQLite for local development
        # This is the fallback when TEST_DATABASE_URL is not set
        session = test_db()
        result = session.execute(text("SELECT sqlite_version()"))
        version_info = result.fetchone()[0]
        # SQLite version should be a string with dots (e.g., "3.39.4")
        assert isinstance(version_info, str) and "." in version_info
        session.close()


def test_database_transactions(test_db):
    """Test that database transactions work correctly"""
    from app.models.models import User
    from app.auth.auth import get_password_hash
    
    session = test_db()
    
    # Create a test user
    test_user = User(
        username="test_db_user",
        name="Test DB User",
        email="test_db@example.com",
        hashed_password=get_password_hash("password123")
    )
    
    session.add(test_user)
    session.commit()
    
    # Verify the user was created
    found_user = session.query(User).filter(User.username == "test_db_user").first()
    assert found_user is not None
    assert found_user.name == "Test DB User"
    assert found_user.email == "test_db@example.com"
    
    session.close()