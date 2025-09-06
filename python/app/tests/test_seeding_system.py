"""
Test the database seeding system
"""
import pytest
from app.seeds.manager import SeedManager
from app.models.user import User
from app.models.blog_post import BlogPost
from app.models.comment import Comment


class TestSeedingSystem:
    """Test the seeding system functionality"""
    
    def test_seeder_creates_users(self, test_db):
        """Test that the user seeder creates expected users"""
        # Create seed manager
        manager = SeedManager(test_db)
        
        # Run seeding
        manager.seed_up()
        
        # Check that users were created
        # Get the actual session from the manager
        session = manager.db
        admin_user = session.query(User).filter(User.username == "admin").first()
        editor_user = session.query(User).filter(User.username == "editor").first()
        user1 = session.query(User).filter(User.username == "user1").first()
        
        assert admin_user is not None
        assert editor_user is not None
        assert user1 is not None
        
        assert admin_user.email == "admin@blogapp.com"
        assert editor_user.email == "editor@blogapp.com"
        assert user1.email == "user1@blogapp.com"
    
    def test_seeder_creates_posts(self, test_db):
        """Test that the post seeder creates expected posts"""
        manager = SeedManager(test_db)
        manager.seed_up()
        
        # Check posts
        session = manager.db
        welcome_post = session.query(BlogPost).filter(BlogPost.slug == "welcome-to-our-blog-platform").first()
        blog_tips_post = session.query(BlogPost).filter(BlogPost.slug == "getting-started-with-blogging").first()
        
        assert welcome_post is not None
        assert blog_tips_post is not None
        
        assert welcome_post.title == "Welcome to Our Blog Platform"
        assert welcome_post.featured is True
    
    def test_seeder_creates_comments(self, test_db):
        """Test that the comment seeder creates expected comments"""
        manager = SeedManager(test_db)
        manager.seed_up()
        
        # Check comments exist
        session = manager.db
        comment_count = session.query(Comment).count()
        assert comment_count > 0
        
        # Check specific comment
        welcome_post = session.query(BlogPost).filter(BlogPost.slug == "welcome-to-our-blog-platform").first()
        comments = session.query(Comment).filter(Comment.blog_post_id == welcome_post.id).all()
        
        assert len(comments) > 0
        assert any("Welcome to the platform" in comment.content for comment in comments)
    
    def test_seeder_is_idempotent(self, test_db):
        """Test that running seeding twice doesn't create duplicates"""
        manager = SeedManager(test_db)
        
        # Run seeding twice
        manager.seed_up()
        
        # Count records after first run
        session = manager.db
        user_count_1 = session.query(User).count()
        post_count_1 = session.query(BlogPost).count()
        comment_count_1 = session.query(Comment).count()
        
        # Create new manager and run again
        manager2 = SeedManager(test_db)
        manager2.seed_up()
        
        # Count should be the same
        session2 = manager2.db
        user_count_2 = session2.query(User).count()
        post_count_2 = session2.query(BlogPost).count()
        comment_count_2 = session2.query(Comment).count()
        
        assert user_count_1 == user_count_2
        assert post_count_1 == post_count_2
        assert comment_count_1 == comment_count_2
