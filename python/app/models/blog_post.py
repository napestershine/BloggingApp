from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base
import enum


class PostStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
    REJECTED = "rejected"
    SCHEDULED = "scheduled"


# Association tables for many-to-many relationships (commented out for now)
# blog_post_tags = Table(
#     'blog_post_tags',
#     Base.metadata,
#     Column('blog_post_id', Integer, ForeignKey('blog_posts.id'), primary_key=True),
#     Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
# )

# blog_post_categories = Table(
#     'blog_post_categories', 
#     Base.metadata,
#     Column('blog_post_id', Integer, ForeignKey('blog_posts.id'), primary_key=True),
#     Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
# )


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
    # likes = relationship("PostLike", back_populates="post")
    # shares = relationship("PostShare", back_populates="post")
    # Note: Tags and categories use simple text fields for now
    # tags = relationship("Tag", secondary=blog_post_tags, back_populates="blog_posts")
    # categories = relationship("Category", secondary=blog_post_categories, back_populates="blog_posts")