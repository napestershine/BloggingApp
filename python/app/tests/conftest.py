import pytest
import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database.connection import get_db, Base


@pytest.fixture(scope="function")
def test_db():
    """Create a temporary test database for each test"""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)
    
    # Create engine for test database
    test_database_url = f"sqlite:///{db_path}"
    engine = create_engine(test_database_url, connect_args={"check_same_thread": False})
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    yield SessionLocal
    
    # Cleanup
    app.dependency_overrides.clear()
    os.unlink(db_path)


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with isolated database"""
    with TestClient(app) as test_client:
        yield test_client