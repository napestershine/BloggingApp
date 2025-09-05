from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

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
    pass

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[PostStatus] = None

class BlogPostInDB(BlogPostBase):
    id: int
    published: datetime
    last_modified: datetime
    author_id: int
    
    class Config:
        from_attributes = True

class BlogPost(BlogPostInDB):
    author: User
    comments: List["Comment"] = []
    categories: List["Category"] = []
    tags: List["Tag"] = []

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

# Media schemas
class MediaBase(BaseModel):
    filename: str
    original_filename: str
    file_size: int
    mime_type: str

class MediaCreate(MediaBase):
    file_path: str

class MediaInDB(MediaBase):
    id: int
    file_path: str
    uploaded_at: datetime
    uploaded_by: int
    
    class Config:
        from_attributes = True

class Media(MediaInDB):
    uploader: User

# Category schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    slug: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None

class CategoryInDB(CategoryBase):
    id: int
    slug: str
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

class Category(CategoryInDB):
    creator: User

# Tag schemas  
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagInDB(TagBase):
    id: int
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

class Tag(TagInDB):
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

# Update forward references after all classes are defined
BlogPost.model_rebuild()
Comment.model_rebuild()