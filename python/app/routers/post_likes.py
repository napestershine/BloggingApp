from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.connection import get_db
from app.models.models import PostLike, BlogPost, User, ReactionType
from app.schemas.schemas import (
    PostLikeCreate, 
    PostReactionsSummary, 
    ReactionTypeEnum
)
from app.auth.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["post_likes"])

@router.post("/{post_id}/like", response_model=PostReactionsSummary, status_code=status.HTTP_201_CREATED)
def like_post(
    post_id: int,
    like_data: PostLikeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Like or react to a post. If user already reacted, update the reaction."""
    
    # Check if post exists
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Check if user already liked this post
    existing_like = db.query(PostLike).filter(
        PostLike.user_id == current_user.id,
        PostLike.post_id == post_id
    ).first()
    
    if existing_like:
        # Update existing reaction
        existing_like.reaction_type = ReactionType(like_data.reaction_type.value)
        db.commit()
        db.refresh(existing_like)
    else:
        # Create new reaction
        new_like = PostLike(
            user_id=current_user.id,
            post_id=post_id,
            reaction_type=ReactionType(like_data.reaction_type.value)
        )
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
    
    # Return updated reaction summary
    return get_post_reactions(post_id, db, current_user)

@router.delete("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove user's reaction from a post."""
    
    # Check if post exists
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Find and delete user's reaction
    like = db.query(PostLike).filter(
        PostLike.user_id == current_user.id,
        PostLike.post_id == post_id
    ).first()
    
    if not like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Like not found"
        )
    
    db.delete(like)
    db.commit()

@router.get("/{post_id}/reactions", response_model=PostReactionsSummary)
def get_post_reactions(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get reaction summary for a post."""
    
    # Check if post exists
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Get total reaction count
    total_reactions = db.query(PostLike).filter(PostLike.post_id == post_id).count()
    
    # Get reactions by type
    reaction_counts = db.query(
        PostLike.reaction_type,
        func.count(PostLike.id).label('count')
    ).filter(
        PostLike.post_id == post_id
    ).group_by(PostLike.reaction_type).all()
    
    reactions_by_type = {
        reaction.value: count for reaction, count in reaction_counts
    }
    
    # Get current user's reaction
    user_reaction = None
    if current_user:
        user_like = db.query(PostLike).filter(
            PostLike.user_id == current_user.id,
            PostLike.post_id == post_id
        ).first()
        if user_like:
            user_reaction = ReactionTypeEnum(user_like.reaction_type.value)
    
    return PostReactionsSummary(
        post_id=post_id,
        total_reactions=total_reactions,
        reactions_by_type=reactions_by_type,
        user_reaction=user_reaction
    )