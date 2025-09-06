from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Enum, UniqueConstraint, BigInteger, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base
import enum

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin" 
    SUPER_ADMIN = "super_admin"

# Enums for post status
class PostStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
    REJECTED = "rejected"
    SCHEDULED = "scheduled"

class CommentStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SPAM = "spam"


# Enum for reaction types
class ReactionType(enum.Enum):
    LIKE = "like"
    LOVE = "love"
    LAUGH = "laugh"
    WOW = "wow"
    SAD = "sad"
    ANGRY = "angry"

# Association tables for many-to-many relationships
blog_post_tags = Table(
    'blog_post_tags',
    Base.metadata,
    Column('blog_post_id', Integer, ForeignKey('blog_posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

blog_post_categories = Table(
    'blog_post_categories', 
    Base.metadata,
    Column('blog_post_id', Integer, ForeignKey('blog_posts.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Email verification
    email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(255), nullable=True)
    
    # Password reset
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime(timezone=True), nullable=True)
    
    # Profile fields
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(255), nullable=True)
    social_links = Column(Text, nullable=True)  # JSON string
    
    # WhatsApp notification settings
    whatsapp_number = Column(String(20), nullable=True)
    whatsapp_notifications_enabled = Column(Boolean, default=False)
    notify_on_new_posts = Column(Boolean, default=True)
    notify_on_comments = Column(Boolean, default=True)
    notify_on_mentions = Column(Boolean, default=True)
    
    # Relationships
    posts = relationship("BlogPost", back_populates="author", foreign_keys="BlogPost.author_id")
    comments = relationship("Comment", back_populates="author", foreign_keys="Comment.author_id")

class BlogPost(Base):
    __tablename__ = "blog_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    slug = Column(String(255), unique=True, index=True)
    status = Column(Enum(PostStatus), default=PostStatus.DRAFT, nullable=False)
    published = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Moderation fields
    status = Column(Enum(PostStatus), default=PostStatus.PUBLISHED, nullable=False)
    moderated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    moderated_at = Column(DateTime(timezone=True), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    featured = Column(Boolean, default=False)
    scheduled_publish = Column(DateTime(timezone=True), nullable=True)

    # SEO fields
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    og_title = Column(String(255), nullable=True)
    og_description = Column(String(500), nullable=True)
    og_image = Column(String(255), nullable=True)
    
    # Analytics fields for trending/search
    view_count = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Categories/tags (stored as JSON string for now)
    tags = Column(Text, nullable=True)  # JSON string of tags
    category = Column(String(100), nullable=True)
    
    # Relationships
    author = relationship("User", back_populates="posts", foreign_keys=[author_id])
    comments = relationship("Comment", back_populates="blog_post")
    moderator = relationship("User", foreign_keys=[moderated_by])
    likes = relationship("PostLike", back_populates="post")
    shares = relationship("PostShare", back_populates="post")
    tags = relationship("Tag", secondary=blog_post_tags, back_populates="blog_posts")
    categories = relationship("Category", secondary=blog_post_categories, back_populates="blog_posts")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    published = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blog_post_id = Column(Integer, ForeignKey("blog_posts.id"), nullable=False)

    # Moderation fields
    status = Column(Enum(CommentStatus), default=CommentStatus.PENDING, nullable=False)
    moderated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    moderated_at = Column(DateTime(timezone=True), nullable=True)
    is_spam = Column(Boolean, default=False)
    
    # Relationships
    author = relationship("User", back_populates="comments", foreign_keys=[author_id])
    blog_post = relationship("BlogPost", back_populates="comments")

    # Threading support - parent comment for replies
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    
    # Moderation fields
    is_moderated = Column(Boolean, default=False)
    moderation_reason = Column(String(255), nullable=True)
    moderated_at = Column(DateTime(timezone=True), nullable=True)
    moderated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Self-referential relationship for threading
    parent = relationship("Comment", remote_side=[id], backref="replies")
    moderator = relationship("User", foreign_keys=[moderated_by], post_update=True)

class CommentReaction(Base):
    __tablename__ = "comment_reactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)
    reaction_type = Column(Enum(ReactionType), default=ReactionType.LIKE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    comment = relationship("Comment")
    
    # Ensure a user can only have one reaction per comment
    __table_args__ = (
        UniqueConstraint('user_id', 'comment_id', name='uq_user_comment_reaction'),
    )

class PostLike(Base):
    __tablename__ = "post_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("blog_posts.id"), nullable=False)
    reaction_type = Column(Enum(ReactionType), default=ReactionType.LIKE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    post = relationship("BlogPost", back_populates="likes")
    
    # Ensure a user can only have one reaction per post
    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='uq_user_post_like'),
    )

# Enum for social sharing platforms
class SharingPlatform(enum.Enum):
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    REDDIT = "reddit"
    EMAIL = "email"
    COPY_LINK = "copy_link"
    WHATSAPP = "whatsapp"

class PostShare(Base):
    __tablename__ = "post_shares"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("blog_posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Optional for anonymous shares
    platform = Column(Enum(SharingPlatform), nullable=False)
    shared_at = Column(DateTime(timezone=True), server_default=func.now())
    user_agent = Column(String(500), nullable=True)  # For tracking device/browser
    ip_address = Column(String(45), nullable=True)  # For basic analytics
    
    # Relationships
    post = relationship("BlogPost")
    user = relationship("User")

class Media(Base):
    __tablename__ = "media"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    mime_type = Column(String(100), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    uploader = relationship("User")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    creator = relationship("User")
    blog_posts = relationship("BlogPost", secondary=blog_post_categories, back_populates="categories")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships 
    creator = relationship("User")
    blog_posts = relationship("BlogPost", secondary=blog_post_tags, back_populates="tags")
