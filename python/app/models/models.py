from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base

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
    comments = relationship("Comment", back_populates="author")

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

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    published = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blog_post_id = Column(Integer, ForeignKey("blog_posts.id"), nullable=False)
    
    # Relationships
    author = relationship("User", back_populates="comments")
    blog_post = relationship("BlogPost", back_populates="comments")

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