"""Unit tests for post use cases using in-memory repositories"""
import pytest
from datetime import datetime
from app.use_cases.posts import (
    CreatePostUseCase, UpdatePostUseCase, GetPostUseCase, GetPostBySlugUseCase,
    ListPostsUseCase, DeletePostUseCase, PublishPostUseCase
)
from app.use_cases.posts import CreatePostRequest, UpdatePostRequest, ListPostsRequest
from app.adapters.memory_repositories import InMemoryPostRepository
from app.adapters.services import DefaultSlugGenerator
from app.domain.entities import User, UserRole, PostStatus
from app.domain.errors import PostNotFoundError, UnauthorizedPostAccessError


class TestCreatePostUseCase:
    """Test post creation use case"""
    
    def setup_method(self):
        """Set up test dependencies"""
        self.post_read_repository = InMemoryPostRepository()
        self.post_write_repository = self.post_read_repository  # Same for in-memory
        self.slug_generator = DefaultSlugGenerator()
        self.use_case = CreatePostUseCase(
            self.post_read_repository,
            self.post_write_repository,
            self.slug_generator
        )
        
        # Create test user
        self.test_user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            name="Test User",
            role=UserRole.USER
        )
    
    def test_create_post_success(self):
        """Test successful post creation"""
        request = CreatePostRequest(
            title="Test Post",
            content="This is a test post content",
            author_id=self.test_user.id,
            meta_title="Test Meta Title",
            meta_description="Test meta description"
        )
        
        post = self.use_case.execute(request)
        
        assert post.id is not None
        assert post.title == "Test Post"
        assert post.content == "This is a test post content"
        assert post.slug == "test-post"
        assert post.author_id == self.test_user.id
        assert post.status == PostStatus.DRAFT
        assert post.meta_title == "Test Meta Title"
        assert post.meta_description == "Test meta description"
    
    def test_create_post_unique_slug(self):
        """Test that duplicate titles get unique slugs"""
        # Create first post
        request1 = CreatePostRequest(
            title="Test Post",
            content="First post content",
            author_id=self.test_user.id
        )
        post1 = self.use_case.execute(request1)
        assert post1.slug == "test-post"
        
        # Create second post with same title
        request2 = CreatePostRequest(
            title="Test Post",
            content="Second post content",
            author_id=self.test_user.id
        )
        post2 = self.use_case.execute(request2)
        assert post2.slug == "test-post-1"
    
    def test_create_post_special_characters_in_title(self):
        """Test slug generation with special characters"""
        request = CreatePostRequest(
            title="Test Post with Special Chars! @#$%",
            content="Content",
            author_id=self.test_user.id
        )
        
        post = self.use_case.execute(request)
        assert post.slug == "test-post-with-special-chars"


class TestUpdatePostUseCase:
    """Test post update use case"""
    
    def setup_method(self):
        """Set up test dependencies"""
        self.post_read_repository = InMemoryPostRepository()
        self.post_write_repository = self.post_read_repository
        self.slug_generator = DefaultSlugGenerator()
        
        # Create test users
        self.author = User(
            id=1,
            username="author",
            email="author@example.com", 
            name="Author User",
            role=UserRole.USER
        )
        
        self.admin = User(
            id=2,
            username="admin",
            email="admin@example.com",
            name="Admin User", 
            role=UserRole.ADMIN
        )
        
        self.other_user = User(
            id=3,
            username="other",
            email="other@example.com",
            name="Other User",
            role=UserRole.USER
        )
        
        # Create test post
        create_use_case = CreatePostUseCase(
            self.post_read_repository,
            self.post_write_repository,
            self.slug_generator
        )
        
        create_request = CreatePostRequest(
            title="Original Title",
            content="Original content",
            author_id=self.author.id
        )
        self.test_post = create_use_case.execute(create_request)
        
        self.use_case = UpdatePostUseCase(
            self.post_read_repository,
            self.post_write_repository,
            self.slug_generator
        )
    
    def test_update_post_by_author(self):
        """Test successful post update by author"""
        request = UpdatePostRequest(
            post_id=self.test_post.id,
            title="Updated Title",
            content="Updated content"
        )
        
        updated_post = self.use_case.execute(request, self.author)
        
        assert updated_post.title == "Updated Title"
        assert updated_post.content == "Updated content"
        assert updated_post.slug == "updated-title"
    
    def test_update_post_by_admin(self):
        """Test post update by admin"""
        request = UpdatePostRequest(
            post_id=self.test_post.id,
            title="Admin Updated Title"
        )
        
        updated_post = self.use_case.execute(request, self.admin)
        assert updated_post.title == "Admin Updated Title"
    
    def test_update_post_unauthorized(self):
        """Test unauthorized post update"""
        request = UpdatePostRequest(
            post_id=self.test_post.id,
            title="Unauthorized Update"
        )
        
        with pytest.raises(UnauthorizedPostAccessError):
            self.use_case.execute(request, self.other_user)
    
    def test_update_nonexistent_post(self):
        """Test updating non-existent post"""
        request = UpdatePostRequest(
            post_id=999,
            title="New Title"
        )
        
        with pytest.raises(PostNotFoundError):
            self.use_case.execute(request, self.author)


class TestGetPostUseCase:
    """Test get post use case"""
    
    def setup_method(self):
        """Set up test dependencies"""
        self.post_read_repository = InMemoryPostRepository()
        self.post_write_repository = self.post_read_repository
        self.slug_generator = DefaultSlugGenerator()
        
        # Create test post
        create_use_case = CreatePostUseCase(
            self.post_read_repository,
            self.post_write_repository,
            self.slug_generator
        )
        
        create_request = CreatePostRequest(
            title="Test Post",
            content="Test content",
            author_id=1,
            status=PostStatus.PUBLISHED
        )
        self.test_post = create_use_case.execute(create_request)
        
        self.use_case = GetPostUseCase(
            self.post_read_repository,
            self.post_write_repository
        )
    
    def test_get_post_success(self):
        """Test successful post retrieval"""
        post = self.use_case.execute(self.test_post.id, increment_views=False)
        
        assert post.id == self.test_post.id
        assert post.title == "Test Post"
        # Don't check view_count here since other tests might affect it
    
    def test_get_post_increment_views(self):
        """Test post retrieval with view count increment"""
        # First get the post without incrementing to get current count
        current_post = self.use_case.execute(self.test_post.id, increment_views=False)
        initial_views = current_post.view_count
        
        # Now get with increment
        post = self.use_case.execute(self.test_post.id, increment_views=True)
        
        assert post.view_count == initial_views + 1
    
    def test_get_nonexistent_post(self):
        """Test getting non-existent post"""
        with pytest.raises(PostNotFoundError):
            self.use_case.execute(999)


class TestListPostsUseCase:
    """Test list posts use case"""
    
    def setup_method(self):
        """Set up test dependencies"""
        self.post_read_repository = InMemoryPostRepository()
        self.post_write_repository = self.post_read_repository
        self.slug_generator = DefaultSlugGenerator()
        
        # Create test posts
        create_use_case = CreatePostUseCase(
            self.post_read_repository,
            self.post_write_repository,
            self.slug_generator
        )
        
        # Published posts
        for i in range(3):
            request = CreatePostRequest(
                title=f"Published Post {i}",
                content=f"Content {i}",
                author_id=1,
                status=PostStatus.PUBLISHED
            )
            create_use_case.execute(request)
        
        # Draft posts
        for i in range(2):
            request = CreatePostRequest(
                title=f"Draft Post {i}",
                content=f"Draft Content {i}",
                author_id=1,
                status=PostStatus.DRAFT
            )
            create_use_case.execute(request)
        
        self.use_case = ListPostsUseCase(self.post_read_repository)
    
    def test_list_published_posts(self):
        """Test listing only published posts"""
        request = ListPostsRequest(published_only=True)
        posts = self.use_case.execute(request)
        
        assert len(posts) == 3
        for post in posts:
            assert post.status == PostStatus.PUBLISHED
    
    def test_list_posts_by_author(self):
        """Test listing posts by specific author"""
        request = ListPostsRequest(
            author_id=1,
            published_only=False
        )
        posts = self.use_case.execute(request)
        
        assert len(posts) == 5  # 3 published + 2 draft
        for post in posts:
            assert post.author_id == 1
    
    def test_list_posts_pagination(self):
        """Test post listing with pagination"""
        request = ListPostsRequest(
            published_only=True,
            skip=1,
            limit=2
        )
        posts = self.use_case.execute(request)
        
        assert len(posts) == 2


class TestDeletePostUseCase:
    """Test delete post use case"""
    
    def setup_method(self):
        """Set up test dependencies"""
        self.post_read_repository = InMemoryPostRepository()
        self.post_write_repository = self.post_read_repository
        self.slug_generator = DefaultSlugGenerator()
        
        # Create test users
        self.author = User(id=1, username="author", email="author@example.com", name="Author", role=UserRole.USER)
        self.admin = User(id=2, username="admin", email="admin@example.com", name="Admin", role=UserRole.ADMIN)
        self.other_user = User(id=3, username="other", email="other@example.com", name="Other", role=UserRole.USER)
        
        # Create test post
        create_use_case = CreatePostUseCase(
            self.post_read_repository,
            self.post_write_repository,
            self.slug_generator
        )
        
        create_request = CreatePostRequest(
            title="Test Post",
            content="Test content",
            author_id=self.author.id
        )
        self.test_post = create_use_case.execute(create_request)
        
        self.use_case = DeletePostUseCase(
            self.post_read_repository,
            self.post_write_repository
        )
    
    def test_delete_post_by_author(self):
        """Test successful post deletion by author"""
        result = self.use_case.execute(self.test_post.id, self.author)
        assert result is True
        
        # Verify post is deleted
        assert self.post_read_repository.get_by_id(self.test_post.id) is None
    
    def test_delete_post_by_admin(self):
        """Test post deletion by admin"""
        result = self.use_case.execute(self.test_post.id, self.admin)
        assert result is True
    
    def test_delete_post_unauthorized(self):
        """Test unauthorized post deletion"""
        with pytest.raises(UnauthorizedPostAccessError):
            self.use_case.execute(self.test_post.id, self.other_user)
    
    def test_delete_nonexistent_post(self):
        """Test deleting non-existent post"""
        with pytest.raises(PostNotFoundError):
            self.use_case.execute(999, self.author)