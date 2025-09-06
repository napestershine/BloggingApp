from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.models import UserRole, PostStatus, CommentStatus
from typing import Optional, List, Dict
from enum import Enum

# --- Enum definitions ---
class ReactionTypeEnum(str, Enum):
    LIKE = "like"
    LOVE = "love"
    LAUGH = "laugh"
    WOW = "wow"
    SAD = "sad"
    ANGRY = "angry"

class SharingPlatformEnum(str, Enum):
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    REDDIT = "reddit"
    EMAIL = "email"
    COPY_LINK = "copy_link"
    WHATSAPP = "whatsapp"

class PostStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"

# --- User schemas ---
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
    role: UserRole
    created_at: datetime
    
    class Config:
        from_attributes = True

class User(UserInDB):
    pass

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

# --- Category and Tag schemas ---
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

# --- BlogPost schemas ---
class BlogPostBase(BaseModel):
    title: str
    content: str
    slug: Optional[str] = None
    status: Optional[PostStatus] = PostStatus.DRAFT

class BlogPostCreate(BlogPostBase):
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    tag_ids: Optional[List[int]] = None
    category_ids: Optional[List[int]] = None

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[PostStatus] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    tag_ids: Optional[List[int]] = None
    category_ids: Optional[List[int]] = None

class BlogPostInDB(BlogPostBase):
    id: int
    published: datetime
    last_modified: datetime
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
    total_reactions: Optional[int] = 0
    reactions_by_type: Optional[Dict[str, int]] = {}
    user_reaction: Optional[ReactionTypeEnum] = None
    categories: List["Category"] = []
    tags: List["Tag"] = []

# --- Comment schemas ---
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    blog_post_id: int
    parent_id: Optional[int] = None

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

# --- Other schemas ---
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

class CommentModerationAction(BaseModel):
    action: str
    reason: Optional[str] = None

class PostShareCreate(BaseModel):
    platform: SharingPlatformEnum

class PostShare(BaseModel):
    id: int
    post_id: int
    user_id: Optional[int] = None
    platform: SharingPlatformEnum
    shared_at: datetime
    
    class Config:
        from_attributes = True

class PostShareStats(BaseModel):
    post_id: int
    total_shares: int
    shares_by_platform: Dict[str, int]
    recent_shares: List[PostShare] = []

class PostReactionsSummary(BaseModel):
    post_id: int
    total_reactions: int
    reactions_by_type: Dict[str, int]
    user_reaction: Optional[ReactionTypeEnum] = None

class BlogPostTagsUpdate(BaseModel):
    tag_ids: List[int]

class BlogPostCategoriesUpdate(BaseModel):
    category_ids: List[int]

class DraftAutoSave(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class EmailVerificationRequest(BaseModel):
    email: EmailStr

class EmailVerificationConfirm(BaseModel):
    token: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

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

class SearchQuery(BaseModel):
    q: str
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    sort_by: Optional[str] = "relevance"
    limit: int = 10
    offset: int = 0

class SearchResult(BaseModel):
    posts: List[BlogPost]
    total: int
    suggestions: List[str] = []

class SearchSuggestion(BaseModel):
    query: str
    suggestions: List[str]

class SlugValidation(BaseModel):
    slug: str
    is_available: bool
    suggestions: List[str] = []

class SlugSuggestion(BaseModel):
    title: str
    suggestions: List[str]

class TrendingPost(BaseModel):
    post: BlogPost
    score: float

class RelatedPost(BaseModel):
    post: BlogPost
    similarity_score: float

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

# Update forward references after all classes are defined
BlogPost.model_rebuild()
Comment.model_rebuild()

# Search schemas
class SearchResult(BaseModel):
    """Search result item"""
    title: str
    content: str
    slug: str
    author: str
    published: datetime
    relevance_score: Optional[float] = None

class SearchSuggestion(BaseModel):
    """Search suggestion item"""
    text: str
    type: str  # "title", "category", "tag", "author"
    description: str

# User Follow schemas
class UserFollowCreate(BaseModel):
    """Schema for following a user"""
    pass  # No additional fields needed, user IDs come from URL and auth

class UserFollowResponse(BaseModel):
    """Response when following/unfollowing a user"""
    following_id: int
    follower_id: int
    is_following: bool
    created_at: Optional[datetime] = None

class UserFollowStats(BaseModel):
    """User follow statistics"""
    followers_count: int
    following_count: int
    is_following: Optional[bool] = None  # Only populated when requesting for another user

class FollowerUser(BaseModel):
    """User info for follower/following lists"""
    id: int
    username: str
    name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Notification schemas
class NotificationTypeEnum(str, Enum):
    FOLLOW = "follow"
    POST_LIKE = "post_like"
    POST_COMMENT = "post_comment"
    COMMENT_REPLY = "comment_reply"
    POST_MENTION = "post_mention"
    COMMENT_MENTION = "comment_mention"

class NotificationBase(BaseModel):
    """Base notification schema"""
    type: NotificationTypeEnum
    title: str
    message: str
    related_user_id: Optional[int] = None
    related_post_id: Optional[int] = None
    related_comment_id: Optional[int] = None

class NotificationCreate(NotificationBase):
    """Schema for creating notifications"""
    user_id: int

class NotificationResponse(NotificationBase):
    """Full notification response"""
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None
    
    # Related entity details
    related_user: Optional[FollowerUser] = None
    related_post: Optional[dict] = None  # Basic post info
    
    class Config:
        from_attributes = True

class NotificationUpdate(BaseModel):
    """Schema for updating notifications"""
    is_read: Optional[bool] = None

class NotificationStats(BaseModel):
    """Notification statistics"""
    total_count: int
    unread_count: int

# Bookmark schemas
class BookmarkBase(BaseModel):
    """Base bookmark schema"""
    pass

class BookmarkCreate(BookmarkBase):
    """Schema for creating a bookmark"""
    pass  # post_id comes from URL, user_id from auth

class BookmarkResponse(BaseModel):
    """Bookmark response schema"""
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    post: Optional[dict] = None  # Basic post info
    
    class Config:
        from_attributes = True

class BookmarkStats(BaseModel):
    """Bookmark statistics"""
    total_bookmarks: int
    is_bookmarked: Optional[bool] = None  # For specific post
