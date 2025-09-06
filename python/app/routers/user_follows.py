from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.database.connection import get_db
from app.models.models import User, UserFollow
from app.schemas.schemas import (
    UserFollowCreate,
    UserFollowResponse,
    UserFollowStats,
    FollowerUser
)
from app.auth.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/follow", tags=["user_follows"])

@router.post("/users/{user_id}", response_model=UserFollowResponse, status_code=status.HTTP_201_CREATED)
def follow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Follow a user
    
    - **user_id**: ID of the user to follow
    
    Returns the follow relationship details
    """
    
    # Check if user exists
    user_to_follow = db.query(User).filter(User.id == user_id).first()
    if not user_to_follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent self-following
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot follow yourself"
        )
    
    # Check if already following
    existing_follow = db.query(UserFollow).filter(
        and_(
            UserFollow.follower_id == current_user.id,
            UserFollow.following_id == user_id
        )
    ).first()
    
    if existing_follow:
        # Already following, return existing relationship
        return UserFollowResponse(
            following_id=user_id,
            follower_id=current_user.id,
            is_following=True,
            created_at=existing_follow.created_at
        )
    
    # Create new follow relationship
    new_follow = UserFollow(
        follower_id=current_user.id,
        following_id=user_id
    )
    
    db.add(new_follow)
    db.commit()
    db.refresh(new_follow)
    
    return UserFollowResponse(
        following_id=user_id,
        follower_id=current_user.id,
        is_following=True,
        created_at=new_follow.created_at
    )

@router.delete("/users/{user_id}", response_model=UserFollowResponse)
def unfollow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Unfollow a user
    
    - **user_id**: ID of the user to unfollow
    
    Returns the updated follow status
    """
    
    # Check if user exists
    user_to_unfollow = db.query(User).filter(User.id == user_id).first()
    if not user_to_unfollow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Find existing follow relationship
    follow_to_remove = db.query(UserFollow).filter(
        and_(
            UserFollow.follower_id == current_user.id,
            UserFollow.following_id == user_id
        )
    ).first()
    
    if not follow_to_remove:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not following this user"
        )
    
    # Remove follow relationship
    db.delete(follow_to_remove)
    db.commit()
    
    return UserFollowResponse(
        following_id=user_id,
        follower_id=current_user.id,
        is_following=False,
        created_at=None
    )

@router.get("/users/{user_id}/followers", response_model=List[FollowerUser])
def get_user_followers(
    user_id: int,
    skip: int = Query(0, ge=0, description="Number of followers to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of followers to return"),
    db: Session = Depends(get_db)
):
    """
    Get a user's followers
    
    - **user_id**: ID of the user whose followers to get
    - **skip**: Number of followers to skip (pagination)
    - **limit**: Number of followers to return (max 100)
    
    Returns list of users who follow the specified user
    """
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get followers
    followers = db.query(User).join(
        UserFollow, User.id == UserFollow.follower_id
    ).filter(
        UserFollow.following_id == user_id
    ).offset(skip).limit(limit).all()
    
    return followers

@router.get("/users/{user_id}/following", response_model=List[FollowerUser])
def get_user_following(
    user_id: int,
    skip: int = Query(0, ge=0, description="Number of following to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of following to return"),
    db: Session = Depends(get_db)
):
    """
    Get users that a user is following
    
    - **user_id**: ID of the user whose following list to get
    - **skip**: Number of following to skip (pagination)
    - **limit**: Number of following to return (max 100)
    
    Returns list of users that the specified user follows
    """
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get following
    following = db.query(User).join(
        UserFollow, User.id == UserFollow.following_id
    ).filter(
        UserFollow.follower_id == user_id
    ).offset(skip).limit(limit).all()
    
    return following

@router.get("/users/{user_id}/stats", response_model=UserFollowStats)
def get_user_follow_stats(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get follow statistics for a user
    
    - **user_id**: ID of the user whose stats to get
    
    Returns follower/following counts and whether current user follows this user
    """
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Count followers
    followers_count = db.query(func.count(UserFollow.id)).filter(
        UserFollow.following_id == user_id
    ).scalar()
    
    # Count following
    following_count = db.query(func.count(UserFollow.id)).filter(
        UserFollow.follower_id == user_id
    ).scalar()
    
    # Check if current user follows this user (if not the same user)
    is_following = None
    if current_user.id != user_id:
        is_following = db.query(UserFollow).filter(
            and_(
                UserFollow.follower_id == current_user.id,
                UserFollow.following_id == user_id
            )
        ).first() is not None
    
    return UserFollowStats(
        followers_count=followers_count,
        following_count=following_count,
        is_following=is_following
    )

@router.get("/me/following", response_model=List[FollowerUser])
def get_my_following(
    skip: int = Query(0, ge=0, description="Number of following to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of following to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get users that the current user is following
    
    - **skip**: Number of following to skip (pagination)
    - **limit**: Number of following to return (max 100)
    
    Returns list of users that the current user follows
    """
    
    # Get following
    following = db.query(User).join(
        UserFollow, User.id == UserFollow.following_id
    ).filter(
        UserFollow.follower_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return following

@router.get("/me/followers", response_model=List[FollowerUser])
def get_my_followers(
    skip: int = Query(0, ge=0, description="Number of followers to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of followers to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the current user's followers
    
    - **skip**: Number of followers to skip (pagination)
    - **limit**: Number of followers to return (max 100)
    
    Returns list of users who follow the current user
    """
    
    # Get followers
    followers = db.query(User).join(
        UserFollow, User.id == UserFollow.follower_id
    ).filter(
        UserFollow.following_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return followers