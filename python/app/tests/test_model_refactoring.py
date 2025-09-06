"""
Test to verify that the refactored models work correctly
"""
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import tempfile
import os

from app.models.user import User, UserRole
from app.models.blog_post import BlogPost, PostStatus
from app.models.comment import Comment
from app.models.category import Category
from app.models.tag import Tag
from app.models.media import Media
from app.models.post_engagement import PostLike, PostShare
from app.database.connection import Base


def test_model_imports():
    """Test that all models can be imported from their separate files"""
    # This test passes if imports work - no assertions needed
    assert User.__name__ == "User"
    assert BlogPost.__name__ == "BlogPost"
    assert Comment.__name__ == "Comment"
    assert Category.__name__ == "Category"
    assert Tag.__name__ == "Tag"
    assert Media.__name__ == "Media"
    assert PostLike.__name__ == "PostLike"
    assert PostShare.__name__ == "PostShare"


def test_backward_compatibility_imports():
    """Test that the old import pattern still works"""
    from app.models.models import User as OldUser, BlogPost as OldBlogPost
    from app.models import User as NewUser, BlogPost as NewBlogPost
    
    # Both import patterns should give the same classes
    assert OldUser is NewUser
    assert OldBlogPost is NewBlogPost


def test_model_creation():
    """Test that models can be instantiated"""
    # Create a temporary database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)
    
    try:
        # Create engine and tables
        engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        
        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            # Create test instances
            user = User(
                username="testuser",
                email="test@example.com", 
                name="Test User",
                hashed_password="hashed",
                role=UserRole.USER
            )
            db.add(user)
            db.commit()
            
            # Verify the user was created
            assert user.id is not None
            assert user.username == "testuser"
            assert user.role == UserRole.USER
            
            # Create a blog post
            post = BlogPost(
                title="Test Post",
                content="Test content",
                author_id=user.id,
                status=PostStatus.PUBLISHED
            )
            db.add(post)
            db.commit()
            
            # Verify the post was created
            assert post.id is not None
            assert post.title == "Test Post"
            assert post.author_id == user.id
            
        finally:
            db.close()
            
    finally:
        # Cleanup
        os.unlink(db_path)


def test_enums():
    """Test that enums are working correctly"""
    assert UserRole.USER == "user"
    assert UserRole.ADMIN == "admin"
    assert PostStatus.DRAFT == "draft"
    assert PostStatus.PUBLISHED == "published"