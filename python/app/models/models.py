from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base
import enum

# Enum for reaction types
class ReactionType(enum.Enum):
    LIKE = "like"
    LOVE = "love"
    LAUGH = "laugh"
    WOW = "wow"
    SAD = "sad"
    ANGRY = "angry"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
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
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="author", foreign_keys="Comment.author_id")

class BlogPost(Base):
    __tablename__ = "blog_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    slug = Column(String(255), unique=True, index=True)
    published = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="blog_post")
    likes = relationship("PostLike", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    published = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blog_post_id = Column(Integer, ForeignKey("blog_posts.id"), nullable=False)
    
    # Threading support - parent comment for replies
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    
    # Moderation fields
    is_moderated = Column(Boolean, default=False)
    moderation_reason = Column(String(255), nullable=True)
    moderated_at = Column(DateTime(timezone=True), nullable=True)
    moderated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    author = relationship("User", back_populates="comments", foreign_keys=[author_id])
    blog_post = relationship("BlogPost", back_populates="comments")
    
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