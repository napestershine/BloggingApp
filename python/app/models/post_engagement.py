from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base
from .comment import ReactionType
import enum


class SharingPlatform(enum.Enum):
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    REDDIT = "reddit"
    EMAIL = "email"
    COPY_LINK = "copy_link"
    WHATSAPP = "whatsapp"


class PostLike(Base):
    __tablename__ = "post_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("blog_posts.id"), nullable=False)
    reaction_type = Column(Enum(ReactionType), default=ReactionType.LIKE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    # post = relationship("BlogPost", back_populates="likes")  # Commented out for now
    
    # Ensure a user can only have one reaction per post
    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='uq_user_post_like'),
    )


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
    # post = relationship("BlogPost", back_populates="shares")  # Commented out for now
    user = relationship("User")