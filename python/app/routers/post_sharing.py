from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.connection import get_db
from app.models.models import PostShare, BlogPost, User, SharingPlatform
from app.schemas.schemas import (
    PostShareCreate, 
    PostShareStats,
    PostShare as PostShareSchema,
    SharingPlatformEnum
)
from app.auth.auth import get_current_user_optional

router = APIRouter(prefix="/posts", tags=["post_sharing"])

@router.post("/{post_id}/share", response_model=PostShareSchema, status_code=status.HTTP_201_CREATED)
def share_post(
    post_id: int,
    share_data: PostShareCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Record a post share event"""
    
    # Check if post exists
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Extract basic analytics info from request
    user_agent = request.headers.get("user-agent", "")[:500]  # Limit length
    ip_address = request.client.host if request.client else None
    
    # Create share record
    db_share = PostShare(
        post_id=post_id,
        user_id=current_user.id if current_user else None,
        platform=SharingPlatform(share_data.platform.value),
        user_agent=user_agent,
        ip_address=ip_address
    )
    
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    
    return db_share

@router.get("/{post_id}/share-stats", response_model=PostShareStats)
def get_post_share_stats(
    post_id: int,
    include_recent: bool = True,
    recent_limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get sharing statistics for a post"""
    
    # Check if post exists
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Get total share count
    total_shares = db.query(PostShare).filter(PostShare.post_id == post_id).count()
    
    # Get shares by platform
    platform_counts = db.query(
        PostShare.platform,
        func.count(PostShare.id).label('count')
    ).filter(
        PostShare.post_id == post_id
    ).group_by(PostShare.platform).all()
    
    shares_by_platform = {
        platform.value: count for platform, count in platform_counts
    }
    
    # Get recent shares if requested
    recent_shares = []
    if include_recent and total_shares > 0:
        recent_shares_query = db.query(PostShare).filter(
            PostShare.post_id == post_id
        ).order_by(PostShare.shared_at.desc()).limit(recent_limit)
        recent_shares = recent_shares_query.all()
    
    return PostShareStats(
        post_id=post_id,
        total_shares=total_shares,
        shares_by_platform=shares_by_platform,
        recent_shares=recent_shares
    )

@router.get("/{post_id}/shares", response_model=List[PostShareSchema])
def get_post_shares(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    platform: Optional[SharingPlatformEnum] = None,
    db: Session = Depends(get_db)
):
    """Get detailed share records for a post (with pagination and filtering)"""
    
    # Check if post exists
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Build query
    query = db.query(PostShare).filter(PostShare.post_id == post_id)
    
    # Filter by platform if specified
    if platform:
        query = query.filter(PostShare.platform == SharingPlatform(platform.value))
    
    # Apply pagination and ordering
    shares = query.order_by(PostShare.shared_at.desc()).offset(skip).limit(limit).all()
    
    return shares

@router.get("/popular-platforms", response_model=Dict[str, int])
def get_popular_sharing_platforms(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get the most popular sharing platforms across all posts (last N days)"""
    
    from datetime import datetime, timezone, timedelta
    
    # Calculate date threshold
    threshold_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Get platform counts for the specified period
    platform_counts = db.query(
        PostShare.platform,
        func.count(PostShare.id).label('count')
    ).filter(
        PostShare.shared_at >= threshold_date
    ).group_by(PostShare.platform).order_by(func.count(PostShare.id).desc()).all()
    
    return {
        platform.value: count for platform, count in platform_counts
    }