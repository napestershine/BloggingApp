from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum

# Reaction types enum for API
class ReactionTypeEnum(str, Enum):
    LIKE = "like"
    LOVE = "love"
    LAUGH = "laugh"
    WOW = "wow"
    SAD = "sad"
    ANGRY = "angry"

# Sharing platforms enum for API
class SharingPlatformEnum(str, Enum):
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    REDDIT = "reddit"
    EMAIL = "email"
    COPY_LINK = "copy_link"
    WHATSAPP = "whatsapp"

# Enum definitions
class PostStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    retyped_password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class User(UserInDB):
    pass

# BlogPost schemas  
class BlogPostBase(BaseModel):
    title: str
    content: str
    slug: Optional[str] = None
    status: Optional[PostStatus] = PostStatus.DRAFT
    
class BlogPostCreate(BlogPostBase):
    # SEO fields (optional during creation)
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    tags: Optional[str] = None  # JSON string
    category: Optional[str] = None

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[PostStatus] = None
    # SEO fields
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None

class BlogPostInDB(BlogPostBase):
    id: int
    published: datetime
    author_id: int
    view_count: int = 0
    updated_at: Optional[datetime] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    
    class Config:
        from_attributes = True

class BlogPost(BlogPostInDB):
    author: User
    comments: List["Comment"] = []

# Comment schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    blog_post_id: int

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentInDB(CommentBase):
    id: int
    published: datetime
    author_id: int
    blog_post_id: int
    
    class Config:
        from_attributes = True

class Comment(CommentInDB):
    author: User

# Update forward references
BlogPost.model_rebuild()

# Tag schemas
class TagBase(BaseModel):
    name: str
    description: Optional[str] = None

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TagInDB(TagBase):
    id: int
    created_at: datetime
    creator_id: int
    
    class Config:
        from_attributes = True

class Tag(TagInDB):
    creator: User

# Category schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryInDB(CategoryBase):
    id: int
    created_at: datetime
    creator_id: int
    
    class Config:
        from_attributes = True

class Category(CategoryInDB):
    creator: User

# Blog post tag/category management schemas
class BlogPostTagsUpdate(BaseModel):
    tag_ids: List[int]

class BlogPostCategoriesUpdate(BaseModel):
    category_ids: List[int]

# Draft management schemas
class DraftAutoSave(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# PostStatus schema  
class PostStatusSchema(BaseModel):
    status: PostStatus

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Email verification schemas
class EmailVerificationRequest(BaseModel):
    email: EmailStr

class EmailVerificationConfirm(BaseModel):
    token: str

# Password reset schemas
class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

# User profile schemas
class UserProfile(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    social_links: Optional[dict] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    social_links: Optional[dict] = None

# WhatsApp notification schemas
class WhatsAppSettings(BaseModel):
    whatsapp_number: Optional[str] = None
    whatsapp_notifications_enabled: bool = False
    notify_on_new_posts: bool = True
    notify_on_comments: bool = True
    notify_on_mentions: bool = True

class WhatsAppSettingsUpdate(BaseModel):
    whatsapp_number: Optional[str] = None
    whatsapp_notifications_enabled: Optional[bool] = None
    notify_on_new_posts: Optional[bool] = None
    notify_on_comments: Optional[bool] = None
    notify_on_mentions: Optional[bool] = None

# SEO schemas
class SEOData(BaseModel):
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None

class SEOPreview(BaseModel):
    title: str
    description: str
    url: str
    image: Optional[str] = None

# Search schemas
class SearchQuery(BaseModel):
    q: str  # query string
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    sort_by: Optional[str] = "relevance"  # relevance, date, views
    limit: int = 10
    offset: int = 0

class SearchResult(BaseModel):
    posts: List[BlogPost]
    total: int
    suggestions: List[str] = []

class SearchSuggestion(BaseModel):
    query: str
    suggestions: List[str]

# Slug schemas
class SlugValidation(BaseModel):
    slug: str
    is_available: bool
    suggestions: List[str] = []

class SlugSuggestion(BaseModel):
    title: str
    suggestions: List[str]

# Trending/Related posts schemas
class TrendingPost(BaseModel):
    post: BlogPost
    score: float  # trending score based on views, comments, etc.

class RelatedPost(BaseModel):
    post: BlogPost
    similarity_score: float