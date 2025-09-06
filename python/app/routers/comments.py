from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone
from app.database.connection import get_db
from app.models.models import Comment, User, BlogPost, CommentReaction, ReactionType
from app.schemas.schemas import (
    Comment as CommentSchema, 
    CommentCreate, 
    CommentUpdate,
    CommentReactionCreate,
    CommentReactionsSummary,
    CommentModerationAction,
    ReactionTypeEnum
)
from app.auth.auth import get_current_user
from app.services.notification_service import whatsapp_service
import asyncio
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/", response_model=List[CommentSchema])
def get_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = db.query(Comment).offset(skip).limit(limit).all()
    return comments

@router.post("/", response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: CommentCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Check if blog post exists
    blog_post = db.query(BlogPost).filter(BlogPost.id == comment.blog_post_id).first()
    if not blog_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )
    
    # Check if parent comment exists (for threaded comments)
    if comment.parent_id:
        parent_comment = db.query(Comment).filter(Comment.id == comment.parent_id).first()
        if not parent_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent comment not found"
            )
        # Ensure parent comment belongs to the same post
        if parent_comment.blog_post_id != comment.blog_post_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent comment must belong to the same blog post"
            )
    
    db_comment = Comment(
        content=comment.content,
        blog_post_id=comment.blog_post_id,
        parent_id=comment.parent_id,
        author_id=current_user.id
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    # Send WhatsApp notification to blog post author if they're not the commenter
    try:
        if (blog_post.author_id != current_user.id and 
            blog_post.author.whatsapp_notifications_enabled and
            blog_post.author.whatsapp_number and
            blog_post.author.notify_on_comments):
            
            asyncio.create_task(
                whatsapp_service.notify_new_comment(
                    current_user.name,
                    blog_post.title,
                    comment.content,
                    blog_post.author.whatsapp_number
                )
            )
    except Exception as e:
        # Don't fail the comment creation if notification fails
        logger.error(f"Failed to send WhatsApp notification for new comment: {e}")
    
    return db_comment

@router.get("/{comment_id}", response_model=CommentSchema)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.put("/{comment_id}", response_model=CommentSchema)
def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Only author can update their comment
    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this comment"
        )
    
    # Update content if provided
    if comment_update.content is not None:
        comment.content = comment_update.content
    
    db.commit()
    db.refresh(comment)
    return comment

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Only author can delete their comment
    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment"
        )
    
    db.delete(comment)
    db.commit()
    return

@router.get("/blog_post/{blog_post_id}", response_model=List[CommentSchema])
def get_comments_for_blog_post(blog_post_id: int, db: Session = Depends(get_db)):
    # Check if blog post exists
    blog_post = db.query(BlogPost).filter(BlogPost.id == blog_post_id).first()
    if not blog_post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    comments = db.query(Comment).filter(Comment.blog_post_id == blog_post_id).all()
    return comments

# New endpoints for advanced comment system

@router.get("/{comment_id}/replies", response_model=List[CommentSchema])
def get_comment_replies(comment_id: int, db: Session = Depends(get_db)):
    """Get all replies to a specific comment"""
    # Check if parent comment exists
    parent_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not parent_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    replies = db.query(Comment).filter(Comment.parent_id == comment_id).all()
    return replies

@router.post("/{comment_id}/reactions", response_model=CommentReactionsSummary, status_code=status.HTTP_201_CREATED)
def react_to_comment(
    comment_id: int,
    reaction_data: CommentReactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """React to a comment with an emoji reaction"""
    # Check if comment exists
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Check if user already reacted to this comment
    existing_reaction = db.query(CommentReaction).filter(
        CommentReaction.user_id == current_user.id,
        CommentReaction.comment_id == comment_id
    ).first()
    
    if existing_reaction:
        # Update existing reaction
        existing_reaction.reaction_type = ReactionType(reaction_data.reaction_type.value)
        db.commit()
        db.refresh(existing_reaction)
    else:
        # Create new reaction
        new_reaction = CommentReaction(
            user_id=current_user.id,
            comment_id=comment_id,
            reaction_type=ReactionType(reaction_data.reaction_type.value)
        )
        db.add(new_reaction)
        db.commit()
        db.refresh(new_reaction)
    
    # Return updated reaction summary
    return get_comment_reactions(comment_id, db, current_user)

@router.delete("/{comment_id}/reactions", status_code=status.HTTP_204_NO_CONTENT)
def remove_comment_reaction(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove user's reaction from a comment"""
    # Check if comment exists
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Find and delete user's reaction
    reaction = db.query(CommentReaction).filter(
        CommentReaction.user_id == current_user.id,
        CommentReaction.comment_id == comment_id
    ).first()
    
    if not reaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reaction not found"
        )
    
    db.delete(reaction)
    db.commit()

@router.get("/{comment_id}/reactions", response_model=CommentReactionsSummary)
def get_comment_reactions(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get reaction summary for a comment"""
    # Check if comment exists
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Get total reaction count
    total_reactions = db.query(CommentReaction).filter(CommentReaction.comment_id == comment_id).count()
    
    # Get reactions by type
    reaction_counts = db.query(
        CommentReaction.reaction_type,
        func.count(CommentReaction.id).label('count')
    ).filter(
        CommentReaction.comment_id == comment_id
    ).group_by(CommentReaction.reaction_type).all()
    
    reactions_by_type = {
        reaction.value: count for reaction, count in reaction_counts
    }
    
    # Get current user's reaction
    user_reaction = None
    if current_user:
        user_reaction_obj = db.query(CommentReaction).filter(
            CommentReaction.user_id == current_user.id,
            CommentReaction.comment_id == comment_id
        ).first()
        if user_reaction_obj:
            user_reaction = ReactionTypeEnum(user_reaction_obj.reaction_type.value)
    
    return CommentReactionsSummary(
        comment_id=comment_id,
        total_reactions=total_reactions,
        reactions_by_type=reactions_by_type,
        user_reaction=user_reaction
    )

@router.post("/{comment_id}/moderate", status_code=status.HTTP_200_OK)
def moderate_comment(
    comment_id: int,
    moderation_action: CommentModerationAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Moderate a comment (hide, approve, or delete)"""
    # Check if comment exists
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Check if user has moderation permissions
    # For now, only the blog post author can moderate comments on their posts
    blog_post = db.query(BlogPost).filter(BlogPost.id == comment.blog_post_id).first()
    if blog_post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to moderate this comment"
        )
    
    if moderation_action.action == "hide":
        comment.is_moderated = True
        comment.moderation_reason = moderation_action.reason or "Hidden by moderator"
        comment.moderated_at = datetime.now(timezone.utc)
        comment.moderated_by = current_user.id
        db.commit()
        return {"message": "Comment hidden successfully"}
    
    elif moderation_action.action == "approve":
        comment.is_moderated = False
        comment.moderation_reason = None
        comment.moderated_at = None
        comment.moderated_by = None
        db.commit()
        return {"message": "Comment approved successfully"}
    
    elif moderation_action.action == "delete":
        db.delete(comment)
        db.commit()
        return {"message": "Comment deleted successfully"}
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid moderation action. Use 'hide', 'approve', or 'delete'"
        )