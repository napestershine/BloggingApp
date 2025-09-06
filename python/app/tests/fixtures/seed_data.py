"""
Pytest fixture for loading minimal seed data for API tests
"""
import pytest
from sqlalchemy.orm import Session
from app.seeds.manager import SeedManager


@pytest.fixture
def seed_data(test_db):
    """
    Fixture that provides minimal seed data for tests.
    
    Uses the same seeders as the CLI but in a test context.
    This ensures consistency between manual testing and automated tests.
    
    Args:
        test_db: The test database session fixture
        
    Returns:
        dict: Dictionary containing references to seeded objects
    """
    # Create a lightweight seeder for testing
    manager = SeedManager()
    manager.db = test_db  # Use the test database session
    
    # Run seeding
    manager.registry.seed_all()
    
    # Return useful objects for tests
    from app.models.user import User
    from app.models.blog_post import BlogPost
    
    admin_user = test_db.query(User).filter(User.username == "admin").first()
    editor_user = test_db.query(User).filter(User.username == "editor").first()
    user1 = test_db.query(User).filter(User.username == "user1").first()
    
    welcome_post = test_db.query(BlogPost).filter(BlogPost.slug == "welcome-to-our-blog-platform").first()
    
    return {
        "admin_user": admin_user,
        "editor_user": editor_user,
        "user1": user1,
        "welcome_post": welcome_post,
        "all_users": [admin_user, editor_user, user1],
        "published_posts": test_db.query(BlogPost).filter(BlogPost.status == "published").all()
    }


@pytest.fixture
def minimal_seed_data(test_db):
    """
    Fixture that provides only the most essential seed data for lightweight tests.
    
    Creates just one admin user and one post for tests that need minimal setup.
    
    Args:
        test_db: The test database session fixture
        
    Returns:
        dict: Dictionary containing minimal seeded objects
    """
    from app.models.user import User, UserRole
    from app.models.blog_post import BlogPost, PostStatus
    from app.auth.auth import get_password_hash
    
    # Create minimal admin user
    admin_user = User(
        username="test_admin",
        email="test_admin@blogapp.com",
        name="Test Admin",
        hashed_password=get_password_hash("test123"),
        role=UserRole.ADMIN,
        email_verified=True
    )
    test_db.add(admin_user)
    test_db.commit()
    test_db.refresh(admin_user)
    
    # Create minimal test post
    test_post = BlogPost(
        title="Test Post",
        content="This is a test post for API testing.",
        slug="test-post",
        status=PostStatus.PUBLISHED,
        author_id=admin_user.id,
        category="Test",
        tags="test,api"
    )
    test_db.add(test_post)
    test_db.commit()
    test_db.refresh(test_post)
    
    return {
        "admin_user": admin_user,
        "test_post": test_post
    }
