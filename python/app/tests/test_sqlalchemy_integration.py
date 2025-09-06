"""Integration tests for SQLAlchemy adapters with real database"""
import pytest
from sqlalchemy.orm import Session
from app.database.connection import get_db, engine
from app.models.models import Base
from app.adapters.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.adapters.sqlalchemy_post_repository import SqlAlchemyPostReadRepository, SqlAlchemyPostWriteRepository
from app.domain.entities import User, UserRole, BlogPost, PostStatus
from app.domain.errors import UserAlreadyExistsError, PostNotFoundError


@pytest.fixture
def db_session():
    """Create a test database session"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Get session
    session = next(get_db())
    
    yield session
    
    # Cleanup
    session.close()


class TestSqlAlchemyUserRepository:
    """Integration tests for SQLAlchemy user repository"""
    
    def test_create_and_get_user(self, db_session: Session):
        """Test creating and retrieving a user"""
        repo = SqlAlchemyUserRepository(db_session)
        
        user = User(
            id=None,
            username="testuser",
            email="test@example.com",
            name="Test User",
            role=UserRole.USER
        )
        
        # Create user with password
        created_user = repo.create(user, "hashed_password_123")
        
        assert created_user.id is not None
        assert created_user.username == "testuser"
        assert created_user.email == "test@example.com"
        
        # Retrieve by ID
        retrieved_user = repo.get_by_id(created_user.id)
        assert retrieved_user is not None
        assert retrieved_user.username == "testuser"
        
        # Retrieve by username
        by_username = repo.get_by_username("testuser")
        assert by_username is not None
        assert by_username.id == created_user.id
        
        # Retrieve by email
        by_email = repo.get_by_email("test@example.com")
        assert by_email is not None
        assert by_email.id == created_user.id
        
        # Check password retrieval
        password = repo.get_hashed_password("testuser")
        assert password == "hashed_password_123"
    
    def test_duplicate_user_creation(self, db_session: Session):
        """Test that duplicate users cannot be created"""
        repo = SqlAlchemyUserRepository(db_session)
        
        user1 = User(
            id=None,
            username="duplicate",
            email="duplicate@example.com",
            name="User 1",
            role=UserRole.USER
        )
        
        # Create first user
        repo.create(user1, "password1")
        
        # Try to create user with same username
        user2 = User(
            id=None,
            username="duplicate",
            email="different@example.com",
            name="User 2",
            role=UserRole.USER
        )
        
        with pytest.raises(UserAlreadyExistsError):
            repo.create(user2, "password2")


class TestSqlAlchemyPostRepository:
    """Integration tests for SQLAlchemy post repositories"""
    
    @pytest.fixture
    def test_user(self, db_session: Session):
        """Create a test user for posts"""
        user_repo = SqlAlchemyUserRepository(db_session)
        
        # Try to get existing user first
        existing_user = user_repo.get_by_username("author")
        if existing_user:
            return existing_user
        
        # Create new user if not exists
        user = User(
            id=None,
            username="author",
            email="author@example.com", 
            name="Author User",
            role=UserRole.USER
        )
        return user_repo.create(user, "password")
    
    def test_create_and_get_post(self, db_session: Session, test_user: User):
        """Test creating and retrieving a post"""
        read_repo = SqlAlchemyPostReadRepository(db_session)
        write_repo = SqlAlchemyPostWriteRepository(db_session)
        
        post = BlogPost(
            id=None,
            title="Test Post",
            content="This is a test post",
            slug="test-post",
            author_id=test_user.id,
            status=PostStatus.PUBLISHED
        )
        
        # Create post
        created_post = write_repo.create(post)
        
        assert created_post.id is not None
        assert created_post.title == "Test Post"
        assert created_post.slug == "test-post"
        
        # Retrieve by ID
        retrieved_post = read_repo.get_by_id(created_post.id)
        assert retrieved_post is not None
        assert retrieved_post.title == "Test Post"
        
        # Retrieve by slug
        by_slug = read_repo.get_by_slug("test-post")
        assert by_slug is not None
        assert by_slug.id == created_post.id
    
    def test_list_published_posts(self, db_session: Session, test_user: User):
        """Test listing published posts"""
        read_repo = SqlAlchemyPostReadRepository(db_session)
        write_repo = SqlAlchemyPostWriteRepository(db_session)
        
        # Create published post
        published_post = BlogPost(
            id=None,
            title="Published Post",
            content="Published content",
            slug="published-post",
            author_id=test_user.id,
            status=PostStatus.PUBLISHED
        )
        write_repo.create(published_post)
        
        # Create draft post
        draft_post = BlogPost(
            id=None,
            title="Draft Post",
            content="Draft content",
            slug="draft-post",
            author_id=test_user.id,
            status=PostStatus.DRAFT
        )
        write_repo.create(draft_post)
        
        # List published posts
        published_posts = read_repo.list_published()
        assert len(published_posts) >= 1
        assert all(post.status == PostStatus.PUBLISHED for post in published_posts)
    
    def test_update_post(self, db_session: Session, test_user: User):
        """Test updating a post"""
        read_repo = SqlAlchemyPostReadRepository(db_session)
        write_repo = SqlAlchemyPostWriteRepository(db_session)
        
        # Create post
        post = BlogPost(
            id=None,
            title="Original Title",
            content="Original content",
            slug="original-title",
            author_id=test_user.id,
            status=PostStatus.DRAFT
        )
        created_post = write_repo.create(post)
        
        # Update post
        created_post.title = "Updated Title"
        created_post.content = "Updated content"
        created_post.status = PostStatus.PUBLISHED
        
        updated_post = write_repo.update(created_post)
        
        assert updated_post.title == "Updated Title"
        assert updated_post.content == "Updated content"
        assert updated_post.status == PostStatus.PUBLISHED
        
        # Verify changes in database
        retrieved_post = read_repo.get_by_id(created_post.id)
        assert retrieved_post.title == "Updated Title"
    
    def test_increment_view_count(self, db_session: Session, test_user: User):
        """Test incrementing post view count"""
        read_repo = SqlAlchemyPostReadRepository(db_session)
        write_repo = SqlAlchemyPostWriteRepository(db_session)
        
        # Create post
        post = BlogPost(
            id=None,
            title="View Count Test",
            content="Content",
            slug="view-count-test",
            author_id=test_user.id,
            status=PostStatus.PUBLISHED,
            view_count=0
        )
        created_post = write_repo.create(post)
        
        initial_views = created_post.view_count
        
        # Increment view count
        write_repo.increment_view_count(created_post.id)
        
        # Check updated count
        updated_post = read_repo.get_by_id(created_post.id)
        assert updated_post.view_count == initial_views + 1