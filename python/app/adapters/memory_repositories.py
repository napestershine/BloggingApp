"""In-memory implementations for testing"""
from typing import Dict, List, Optional
from app.domain.entities import User, BlogPost, Tag, Category
from app.domain.errors import UserNotFoundError, PostNotFoundError
from app.ports.repositories import UserRepository, PostReadRepository, PostWriteRepository


class InMemoryUserRepository:
    """In-memory implementation of UserRepository for testing"""
    
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._passwords: Dict[int, str] = {}
        self._next_id = 1
    
    def create(self, user: User, hashed_password: str = None) -> User:
        """Create a new user"""
        user.id = self._next_id
        self._next_id += 1
        self._users[user.id] = user
        if hashed_password:
            self._passwords[user.id] = hashed_password
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self._users.get(user_id)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        for user in self._users.values():
            if user.username == username:
                return user
        return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        for user in self._users.values():
            if user.email == email:
                return user
        return None
    
    def get_hashed_password(self, username_or_email: str) -> Optional[str]:
        """Get hashed password for authentication"""
        user = self.get_by_username(username_or_email)
        if not user:
            user = self.get_by_email(username_or_email)
        if user:
            return self._passwords.get(user.id)
        return None
    
    def update(self, user: User) -> User:
        """Update existing user"""
        if not user.id or user.id not in self._users:
            raise UserNotFoundError(str(user.id))
        self._users[user.id] = user
        return user
    
    def delete(self, user_id: int) -> bool:
        """Delete user by ID"""
        if user_id in self._users:
            del self._users[user_id]
            if user_id in self._passwords:
                del self._passwords[user_id]
            return True
        return False


class InMemoryPostRepository:
    """In-memory implementation of Post repositories for testing"""
    
    def __init__(self):
        self._posts: Dict[int, BlogPost] = {}
        self._next_id = 1
    
    def create(self, post: BlogPost) -> BlogPost:
        """Create a new post"""
        post.id = self._next_id
        self._next_id += 1
        self._posts[post.id] = post
        return post
    
    def get_by_id(self, post_id: int) -> Optional[BlogPost]:
        """Get post by ID"""
        return self._posts.get(post_id)
    
    def get_by_slug(self, slug: str) -> Optional[BlogPost]:
        """Get post by slug"""
        for post in self._posts.values():
            if post.slug == slug:
                return post
        return None
    
    def list_published(
        self, 
        skip: int = 0, 
        limit: int = 100,
        author_id: Optional[int] = None
    ) -> List[BlogPost]:
        """List published posts"""
        posts = [
            post for post in self._posts.values() 
            if post.is_published() and (not author_id or post.author_id == author_id)
        ]
        return posts[skip:skip + limit]
    
    def list_by_author(
        self, 
        author_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[BlogPost]:
        """List posts by author (including drafts)"""
        posts = [post for post in self._posts.values() if post.author_id == author_id]
        return posts[skip:skip + limit]
    
    def search(
        self, 
        query: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[BlogPost]:
        """Search posts by title/content"""
        posts = [
            post for post in self._posts.values()
            if post.is_published() and (
                query.lower() in post.title.lower() or 
                query.lower() in post.content.lower()
            )
        ]
        return posts[skip:skip + limit]
    
    def update(self, post: BlogPost) -> BlogPost:
        """Update existing post"""
        if not post.id or post.id not in self._posts:
            raise PostNotFoundError(str(post.id))
        self._posts[post.id] = post
        return post
    
    def delete(self, post_id: int) -> bool:
        """Delete post by ID"""
        if post_id in self._posts:
            del self._posts[post_id]
            return True
        return False
    
    def increment_view_count(self, post_id: int) -> None:
        """Increment post view count"""
        if post_id in self._posts:
            self._posts[post_id].view_count += 1