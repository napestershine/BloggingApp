# This file maintains backward compatibility by re-importing from the new modular structure
# All models have been moved to separate files for better organization

# For now, import from the backup until modular files are created
try:
    from .user import User, UserRole
    from .blog_post import BlogPost, PostStatus, blog_post_tags, blog_post_categories
    from .comment import Comment, CommentStatus, CommentReaction, ReactionType
    from .media import Media
    from .category import Category
    from .tag import Tag
    from .post_engagement import PostLike, PostShare, SharingPlatform
except ImportError:
    # Fallback to inline definitions for compatibility
    from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Enum, UniqueConstraint, BigInteger, Table
    from sqlalchemy.orm import relationship
    from sqlalchemy.sql import func
    from app.database.connection import Base
    import enum

    # Admin role enum
    class UserRole(enum.Enum):
        USER = "user"
        ADMIN = "admin"
        SUPER_ADMIN = "super_admin"

    # Post status enum
    class PostStatus(enum.Enum):
        DRAFT = "draft"
        PENDING = "pending"
        PUBLISHED = "published"
        REJECTED = "rejected"
        SCHEDULED = "scheduled"

    # Comment status enum
    class CommentStatus(enum.Enum):
        PENDING = "pending"
        APPROVED = "approved"
        REJECTED = "rejected"
        SPAM = "spam"

    # Reaction types enum
    class ReactionType(enum.Enum):
        LIKE = "like"
        LOVE = "love"
        LAUGH = "laugh"
        WOW = "wow"
        SAD = "sad"
        ANGRY = "angry"

    # Sharing platform enum
    class SharingPlatform(enum.Enum):
        TWITTER = "twitter"
        FACEBOOK = "facebook"
        LINKEDIN = "linkedin"
        REDDIT = "reddit"
        EMAIL = "email"
        COPY_LINK = "copy_link"
        WHATSAPP = "whatsapp"

    # Association tables
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

    # User model
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

    # BlogPost model
    class BlogPost(Base):
        __tablename__ = "blog_posts"
        
        id = Column(Integer, primary_key=True, index=True)
        title = Column(String(255), nullable=False)
        content = Column(Text, nullable=False)
        slug = Column(String(255), unique=True, index=True)
        author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
        status = Column(Enum(PostStatus), default=PostStatus.DRAFT)
        
        # Relationships
        author = relationship("User", back_populates="blog_posts")
        comments = relationship("Comment", back_populates="blog_post", cascade="all, delete-orphan")
        tags = relationship("Tag", secondary=blog_post_tags, back_populates="blog_posts")
        categories = relationship("Category", secondary=blog_post_categories, back_populates="blog_posts")

    # Comment model
    class Comment(Base):
        __tablename__ = "comments"
        
        id = Column(Integer, primary_key=True, index=True)
        content = Column(Text, nullable=False)
        author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        blog_post_id = Column(Integer, ForeignKey("blog_posts.id"), nullable=False)
        parent_comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
        status = Column(Enum(CommentStatus), default=CommentStatus.PENDING)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
        
        # Relationships
        author = relationship("User")
        blog_post = relationship("BlogPost", back_populates="comments")
        parent_comment = relationship("Comment", remote_side=[id], back_populates="replies")
        replies = relationship("Comment", back_populates="parent_comment", cascade="all, delete-orphan")

    # Comment reaction model
    class CommentReaction(Base):
        __tablename__ = "comment_reactions"
        
        id = Column(Integer, primary_key=True, index=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)
        reaction_type = Column(Enum(ReactionType), nullable=False)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        
        # Ensure one reaction per user per comment
        __table_args__ = (UniqueConstraint('user_id', 'comment_id', name='unique_user_comment_reaction'),)
        
        # Relationships
        user = relationship("User")
        comment = relationship("Comment", back_populates="reactions")

    # Media model
    class Media(Base):
        __tablename__ = "media"
        
        id = Column(Integer, primary_key=True, index=True)
        filename = Column(String(255), nullable=False)
        original_filename = Column(String(255), nullable=False)
        file_path = Column(String(500), nullable=False)
        file_size = Column(BigInteger, nullable=False)
        mime_type = Column(String(100), nullable=False)
        uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        
        # Relationships
        uploader = relationship("User")

    # Category model
    class Category(Base):
        __tablename__ = "categories"
        
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String(100), unique=True, nullable=False)
        slug = Column(String(100), unique=True, nullable=False)
        description = Column(Text)
        parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        
        # Relationships
        parent = relationship("Category", remote_side=[id], back_populates="children")
        children = relationship("Category", back_populates="parent", cascade="all, delete-orphan")
        blog_posts = relationship("BlogPost", secondary=blog_post_categories, back_populates="categories")

    # Tag model
    class Tag(Base):
        __tablename__ = "tags"
        
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String(100), unique=True, nullable=False)
        slug = Column(String(100), unique=True, nullable=False)
        description = Column(Text)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        
        # Relationships
        blog_posts = relationship("BlogPost", secondary=blog_post_tags, back_populates="tags")

    # Post engagement models
    class PostLike(Base):
        __tablename__ = "post_likes"
        
        id = Column(Integer, primary_key=True, index=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        blog_post_id = Column(Integer, ForeignKey("blog_posts.id"), nullable=False)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        
        # Ensure one like per user per post
        __table_args__ = (UniqueConstraint('user_id', 'blog_post_id', name='unique_user_post_like'),)
        
        # Relationships
        user = relationship("User")
        blog_post = relationship("BlogPost", back_populates="likes")

    class PostShare(Base):
        __tablename__ = "post_shares"
        
        id = Column(Integer, primary_key=True, index=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        blog_post_id = Column(Integer, ForeignKey("blog_posts.id"), nullable=False)
        platform = Column(Enum(SharingPlatform), nullable=False)
        shared_at = Column(DateTime(timezone=True), server_default=func.now())
        
        # Relationships
        user = relationship("User")
        blog_post = relationship("BlogPost", back_populates="shares")

    # Add missing relationships
    User.blog_posts = relationship("BlogPost", back_populates="author")
    BlogPost.likes = relationship("PostLike", back_populates="blog_post")
    BlogPost.shares = relationship("PostShare", back_populates="blog_post")
    Comment.reactions = relationship("CommentReaction", back_populates="comment")

# Import Base for table creation in main.py
from app.database.connection import Base

# Social features models - inline definitions for now
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Enum, UniqueConstraint, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Notification types enum
class NotificationType(enum.Enum):
    FOLLOW = "follow"
    POST_LIKE = "post_like"
    POST_COMMENT = "post_comment"
    POST_SHARE = "post_share"
    COMMENT_LIKE = "comment_like"
    COMMENT_REPLY = "comment_reply"
    MENTION = "mention"
    SYSTEM = "system"

class UserFollow(Base):
    __tablename__ = "user_follows"
    
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    following_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Ensure unique follower-following pairs
    __table_args__ = (UniqueConstraint('follower_id', 'following_id', name='unique_user_follow'),)
    
    # Relationships
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Optional foreign keys for related objects
    blog_post_id = Column(Integer, ForeignKey('blog_posts.id'), nullable=True)
    comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    
    # WhatsApp notification tracking
    whatsapp_sent = Column(Boolean, default=False, nullable=False)
    whatsapp_sent_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="notifications_received")
    sender = relationship("User", foreign_keys=[sender_id], back_populates="notifications_sent")
    blog_post = relationship("BlogPost", back_populates="notifications")
    comment = relationship("Comment", back_populates="notifications")

class Bookmark(Base):
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    blog_post_id = Column(Integer, ForeignKey('blog_posts.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Ensure unique user-post bookmark pairs
    __table_args__ = (UniqueConstraint('user_id', 'blog_post_id', name='unique_user_bookmark'),)
    
    # Relationships
    user = relationship("User", back_populates="bookmarks")
    blog_post = relationship("BlogPost", back_populates="bookmarks")

# Add relationship properties to existing models
# These would normally be in the individual model files but adding here for compatibility

# Add to User model
User.following = relationship("UserFollow", foreign_keys="UserFollow.follower_id", back_populates="follower")
User.followers = relationship("UserFollow", foreign_keys="UserFollow.following_id", back_populates="following")
User.notifications_received = relationship("Notification", foreign_keys="Notification.recipient_id", back_populates="recipient")
User.notifications_sent = relationship("Notification", foreign_keys="Notification.sender_id", back_populates="sender")
User.bookmarks = relationship("Bookmark", back_populates="user")

# Add to BlogPost model  
BlogPost.notifications = relationship("Notification", back_populates="blog_post")
BlogPost.bookmarks = relationship("Bookmark", back_populates="blog_post")

# Add to Comment model
Comment.notifications = relationship("Notification", back_populates="comment")