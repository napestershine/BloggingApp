from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base
import enum


class CommentStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SPAM = "spam"


class ReactionType(enum.Enum):
    LIKE = "like"
    LOVE = "love"
    LAUGH = "laugh"
    WOW = "wow"
    SAD = "sad"
    ANGRY = "angry"


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