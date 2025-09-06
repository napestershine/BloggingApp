from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.database.connection import get_db
from app.models.models import User, Bookmark, BlogPost, PostStatus
from app.schemas.schemas import (
    BookmarkCreate,
    BookmarkResponse,
    BookmarkStats,
    BlogPost as BlogPostSchema
)
from app.auth.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])

@router.post("/posts/{post_id}", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
def bookmark_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Bookmark a blog post
    
    - **post_id**: ID of the post to bookmark
    
    Returns the bookmark details or existing bookmark if already bookmarked
    """
    
    # Check if post exists and is published
    post = db.query(BlogPost).filter(
        and_(
            BlogPost.id == post_id,
            BlogPost.status == PostStatus.PUBLISHED
        )
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or not published"
        )
    
    # Check if already bookmarked
    existing_bookmark = db.query(Bookmark).filter(
        and_(
            Bookmark.user_id == current_user.id,
            Bookmark.post_id == post_id
        )
    ).first()
    
    if existing_bookmark:
        # Return existing bookmark
        return BookmarkResponse(
            id=existing_bookmark.id,
            user_id=existing_bookmark.user_id,
            post_id=existing_bookmark.post_id,
            created_at=existing_bookmark.created_at,
            post={
                "id": post.id,
                "title": post.title,
                "slug": post.slug,
                "author": post.author.name
            }
        )
    
    # Create new bookmark
    new_bookmark = Bookmark(
        user_id=current_user.id,
        post_id=post_id
    )
    
    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)
    
    return BookmarkResponse(
        id=new_bookmark.id,
        user_id=new_bookmark.user_id,
        post_id=new_bookmark.post_id,
        created_at=new_bookmark.created_at,
        post={
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "author": post.author.name
        }
    )

@router.delete("/posts/{post_id}")
def remove_bookmark(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove a bookmark
    
    - **post_id**: ID of the post to unbookmark
    
    Returns success message
    """
    
    # Find the bookmark
    bookmark = db.query(Bookmark).filter(
        and_(
            Bookmark.user_id == current_user.id,
            Bookmark.post_id == post_id
        )
    ).first()
    
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )
    
    db.delete(bookmark)
    db.commit()
    
    return {"message": "Bookmark removed successfully"}

@router.get("/", response_model=List[BlogPostSchema])
def get_user_bookmarks(
    skip: int = Query(0, ge=0, description="Number of bookmarks to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of bookmarks to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's bookmarked posts
    
    - **skip**: Number of bookmarks to skip (pagination)
    - **limit**: Number of bookmarks to return (max 100)
    
    Returns list of bookmarked blog posts
    """
    
    # Get bookmarked posts
    bookmarked_posts = db.query(BlogPost).join(
        Bookmark, BlogPost.id == Bookmark.post_id
    ).filter(
        and_(
            Bookmark.user_id == current_user.id,
            BlogPost.status == PostStatus.PUBLISHED
        )
    ).order_by(Bookmark.created_at.desc()).offset(skip).limit(limit).all()
    
    return bookmarked_posts

@router.get("/posts/{post_id}", response_model=BookmarkStats)
def get_post_bookmark_stats(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get bookmark statistics for a specific post
    
    - **post_id**: ID of the post
    
    Returns bookmark count and whether current user has bookmarked the post
    """
    
    # Check if post exists
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Count total bookmarks for this post
    total_bookmarks = db.query(func.count(Bookmark.id)).filter(
        Bookmark.post_id == post_id
    ).scalar()
    
    # Check if current user has bookmarked this post
    is_bookmarked = db.query(Bookmark).filter(
        and_(
            Bookmark.user_id == current_user.id,
            Bookmark.post_id == post_id
        )
    ).first() is not None
    
    return BookmarkStats(
        total_bookmarks=total_bookmarks,
        is_bookmarked=is_bookmarked
    )

@router.get("/stats", response_model=BookmarkStats)
def get_user_bookmark_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get bookmark statistics for the current user
    
    Returns total number of bookmarks for the current user
    """
    
    # Count user's total bookmarks
    total_bookmarks = db.query(func.count(Bookmark.id)).filter(
        Bookmark.user_id == current_user.id
    ).scalar()
    
    return BookmarkStats(
        total_bookmarks=total_bookmarks,
        is_bookmarked=None
    )

@router.get("/recent", response_model=List[BlogPostSchema])
def get_recent_bookmarks(
    limit: int = Query(5, ge=1, le=20, description="Number of recent bookmarks to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's most recently bookmarked posts
    
    - **limit**: Number of recent bookmarks to return (max 20)
    
    Returns list of recently bookmarked blog posts
    """
    
    # Get most recently bookmarked posts
    recent_bookmarks = db.query(BlogPost).join(
        Bookmark, BlogPost.id == Bookmark.post_id
    ).filter(
        and_(
            Bookmark.user_id == current_user.id,
            BlogPost.status == PostStatus.PUBLISHED
        )
    ).order_by(Bookmark.created_at.desc()).limit(limit).all()
    
    return recent_bookmarks