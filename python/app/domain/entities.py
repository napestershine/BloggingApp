"""Domain entities - pure Python objects representing business concepts"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class PostStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
    REJECTED = "rejected"
    SCHEDULED = "scheduled"


@dataclass
class User:
    """User domain entity"""
    id: Optional[int]
    username: str
    email: str
    name: str
    role: UserRole = UserRole.USER
    created_at: Optional[datetime] = None
    email_verified: bool = False
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    whatsapp_number: Optional[str] = None
    whatsapp_notifications_enabled: bool = False
    
    def is_admin(self) -> bool:
        return self.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]
    
    def can_moderate_posts(self) -> bool:
        return self.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]


@dataclass 
class BlogPost:
    """Blog post domain entity"""
    id: Optional[int]
    title: str
    content: str
    slug: Optional[str]
    author_id: int
    status: PostStatus = PostStatus.DRAFT
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    view_count: int = 0
    featured: bool = False
    
    def is_published(self) -> bool:
        return self.status == PostStatus.PUBLISHED
    
    def can_be_published(self) -> bool:
        return self.status in [PostStatus.DRAFT, PostStatus.PENDING]
    
    def publish(self) -> None:
        if not self.can_be_published():
            raise ValueError(f"Cannot publish post with status {self.status}")
        self.status = PostStatus.PUBLISHED
        if not self.published_at:
            self.published_at = datetime.now()


@dataclass
class Tag:
    """Tag domain entity"""
    id: Optional[int]
    name: str
    slug: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class Category:
    """Category domain entity"""
    id: Optional[int]
    name: str
    slug: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None