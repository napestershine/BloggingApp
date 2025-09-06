"""Repository port interfaces using Protocol for type safety"""
from typing import Protocol, List, Optional
from app.domain.entities import User, BlogPost, Tag, Category


class UserRepository(Protocol):
    """User repository interface"""
    
    def create(self, user: User) -> User:
        """Create a new user"""
        ...
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        ...
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        ...
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        ...
    
    def update(self, user: User) -> User:
        """Update existing user"""
        ...
    
    def delete(self, user_id: int) -> bool:
        """Delete user by ID"""
        ...


class PostReadRepository(Protocol):
    """Post read operations interface"""
    
    def get_by_id(self, post_id: int) -> Optional[BlogPost]:
        """Get post by ID"""
        ...
    
    def get_by_slug(self, slug: str) -> Optional[BlogPost]:
        """Get post by slug"""
        ...
    
    def list_published(
        self, 
        skip: int = 0, 
        limit: int = 100,
        author_id: Optional[int] = None
    ) -> List[BlogPost]:
        """List published posts"""
        ...
    
    def list_by_author(
        self, 
        author_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[BlogPost]:
        """List posts by author (including drafts if same author)"""
        ...
    
    def search(
        self, 
        query: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[BlogPost]:
        """Search posts by title/content"""
        ...


class PostWriteRepository(Protocol):
    """Post write operations interface"""
    
    def create(self, post: BlogPost) -> BlogPost:
        """Create a new post"""
        ...
    
    def update(self, post: BlogPost) -> BlogPost:
        """Update existing post"""
        ...
    
    def delete(self, post_id: int) -> bool:
        """Delete post by ID"""
        ...
    
    def increment_view_count(self, post_id: int) -> None:
        """Increment post view count"""
        ...


class TagRepository(Protocol):
    """Tag repository interface"""
    
    def create(self, tag: Tag) -> Tag:
        """Create a new tag"""
        ...
    
    def get_by_name(self, name: str) -> Optional[Tag]:
        """Get tag by name"""
        ...
    
    def get_by_slug(self, slug: str) -> Optional[Tag]:
        """Get tag by slug"""
        ...
    
    def list_all(self) -> List[Tag]:
        """List all tags"""
        ...


class CategoryRepository(Protocol):
    """Category repository interface"""
    
    def create(self, category: Category) -> Category:
        """Create a new category"""
        ...
    
    def get_by_name(self, name: str) -> Optional[Category]:
        """Get category by name"""
        ...
    
    def get_by_slug(self, slug: str) -> Optional[Category]:
        """Get category by slug"""
        ...
    
    def list_all(self) -> List[Category]:
        """List all categories"""
        ...