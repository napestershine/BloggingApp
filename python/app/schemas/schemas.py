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

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    slug: Optional[str] = None

class BlogPostInDB(BlogPostBase):
    id: int
    published: datetime
    author_id: int
    
    class Config:
        from_attributes = True

class BlogPost(BlogPostInDB):
    author: User
    comments: List["Comment"] = []
    total_reactions: Optional[int] = 0
    reactions_by_type: Optional[Dict[str, int]] = {}
    user_reaction: Optional[ReactionTypeEnum] = None

# Comment schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    blog_post_id: int
    parent_id: Optional[int] = None  # For threaded comments

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentInDB(CommentBase):
    id: int
    published: datetime
    author_id: int
    blog_post_id: int
    parent_id: Optional[int] = None
    is_moderated: bool = False
    moderation_reason: Optional[str] = None
    moderated_at: Optional[datetime] = None
    moderated_by: Optional[int] = None
    
    class Config:
        from_attributes = True

class Comment(CommentInDB):
    author: User
    replies: List["Comment"] = []
    total_reactions: Optional[int] = 0
    reactions_by_type: Optional[Dict[str, int]] = {}
    user_reaction: Optional[ReactionTypeEnum] = None

# Comment reaction schemas
class CommentReactionCreate(BaseModel):
    reaction_type: ReactionTypeEnum = ReactionTypeEnum.LIKE

class CommentReaction(BaseModel):
    id: int
    user_id: int
    comment_id: int
    reaction_type: ReactionTypeEnum
    created_at: datetime
    
    class Config:
        from_attributes = True

class CommentReactionsSummary(BaseModel):
    comment_id: int
    total_reactions: int
    reactions_by_type: Dict[str, int]
    user_reaction: Optional[ReactionTypeEnum] = None

# Comment moderation schemas
class CommentModerationAction(BaseModel):
    action: str  # "approve", "hide", "delete"
    reason: Optional[str] = None

# Update forward references
BlogPost.model_rebuild()
Comment.model_rebuild()

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

# Post Like schemas
class PostLikeCreate(BaseModel):
    reaction_type: ReactionTypeEnum = ReactionTypeEnum.LIKE

class PostLike(BaseModel):
    id: int
    user_id: int
    post_id: int
    reaction_type: ReactionTypeEnum
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostReactionsSummary(BaseModel):
    post_id: int
    total_reactions: int
    reactions_by_type: Dict[str, int]
    user_reaction: Optional[ReactionTypeEnum] = None