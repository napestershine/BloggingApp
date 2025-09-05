from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
from app.database.connection import get_db
from app.models.models import User, UserRole, BlogPost, Comment
from app.admin.auth import require_admin_role
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

router = APIRouter(prefix="/admin/content", tags=["admin-content"])

class ContentStatus(str, Enum):
    PUBLISHED = "published"
    DRAFT = "draft"
    FLAGGED = "flagged"
    ARCHIVED = "archived"

class PostModerationResponse(BaseModel):
    id: int
    title: str
    content: str
    slug: Optional[str]
    published: datetime
    author_id: int
    author_username: str
    author_name: str
    total_comments: int
    status: str = "published"

class CommentModerationResponse(BaseModel):
    id: int
    content: str
    published: datetime
    author_id: int
    author_username: str
    author_name: str
    blog_post_id: int
    blog_post_title: str
    status: str = "published"

class ContentAction(BaseModel):
    action: str  # "approve", "reject", "flag", "archive"
    reason: Optional[str] = None

@router.get("/posts", response_model=List[PostModerationResponse])
async def get_posts_for_moderation(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    author_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    days: Optional[int] = Query(None, description="Posts from last N days"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_role())
):
    """
    Get posts for content moderation
    """
    query = db.query(BlogPost).join(User, BlogPost.author_id == User.id)
    
    # Apply filters
    if author_id:
        query = query.filter(BlogPost.author_id == author_id)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                BlogPost.title.ilike(search_term),
                BlogPost.content.ilike(search_term)
            )
        )
    
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(BlogPost.published >= cutoff_date)
    
    # Order by most recent first
    posts = query.order_by(desc(BlogPost.published)).offset(skip).limit(limit).all()
    
    result = []
    for post in posts:
        comment_count = db.query(func.count(Comment.id)).filter(
            Comment.blog_post_id == post.id
        ).scalar() or 0
        
        result.append(PostModerationResponse(
            id=post.id,
            title=post.title,
            content=post.content[:500] + "..." if len(post.content) > 500 else post.content,
            slug=post.slug,
            published=post.published,
            author_id=post.author_id,
            author_username=post.author.username,
            author_name=post.author.name,
            total_comments=comment_count
        ))
    
    return result

@router.get("/comments", response_model=List[CommentModerationResponse])
async def get_comments_for_moderation(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    author_id: Optional[int] = Query(None),
    post_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    days: Optional[int] = Query(None, description="Comments from last N days"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_role())
):
    """
    Get comments for content moderation
    """
    query = db.query(Comment).join(User, Comment.author_id == User.id).join(
        BlogPost, Comment.blog_post_id == BlogPost.id
    )
    
    # Apply filters
    if author_id:
        query = query.filter(Comment.author_id == author_id)
    
    if post_id:
        query = query.filter(Comment.blog_post_id == post_id)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(Comment.content.ilike(search_term))
    
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(Comment.published >= cutoff_date)
    
    # Order by most recent first
    comments = query.order_by(desc(Comment.published)).offset(skip).limit(limit).all()
    
    result = []
    for comment in comments:
        result.append(CommentModerationResponse(
            id=comment.id,
            content=comment.content[:200] + "..." if len(comment.content) > 200 else comment.content,
            published=comment.published,
            author_id=comment.author_id,
            author_username=comment.author.username,
            author_name=comment.author.name,
            blog_post_id=comment.blog_post_id,
            blog_post_title=comment.blog_post.title
        ))
    
    return result

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_role())
):
    """
    Delete a blog post (admin only)
    """
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Delete associated comments first
    db.query(Comment).filter(Comment.blog_post_id == post_id).delete()
    db.delete(post)
    db.commit()
    
    return {"message": "Post and associated comments deleted successfully"}

@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_role())
):
    """
    Delete a comment (admin only)
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    db.delete(comment)
    db.commit()
    
    return {"message": "Comment deleted successfully"}

@router.get("/posts/flagged", response_model=List[PostModerationResponse])
async def get_flagged_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_role())
):
    """
    Get flagged posts for review
    Note: This is a placeholder for when flagging system is implemented
    For now, returns recent posts that might need review
    """
    # This would normally filter by flagged status
    # For now, return posts from the last 7 days for review
    cutoff_date = datetime.now() - timedelta(days=7)
    query = db.query(BlogPost).join(User, BlogPost.author_id == User.id).filter(
        BlogPost.published >= cutoff_date
    )
    
    posts = query.order_by(desc(BlogPost.published)).offset(skip).limit(limit).all()
    
    result = []
    for post in posts:
        comment_count = db.query(func.count(Comment.id)).filter(
            Comment.blog_post_id == post.id
        ).scalar() or 0
        
        result.append(PostModerationResponse(
            id=post.id,
            title=post.title,
            content=post.content[:500] + "..." if len(post.content) > 500 else post.content,
            slug=post.slug,
            published=post.published,
            author_id=post.author_id,
            author_username=post.author.username,
            author_name=post.author.name,
            total_comments=comment_count,
            status="flagged"
        ))
    
    return result

@router.get("/analytics/content")
async def get_content_analytics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_role())
):
    """
    Get content analytics for the admin dashboard
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Posts analytics
    total_posts = db.query(func.count(BlogPost.id)).scalar() or 0
    recent_posts = db.query(func.count(BlogPost.id)).filter(
        BlogPost.published >= cutoff_date
    ).scalar() or 0
    
    # Comments analytics
    total_comments = db.query(func.count(Comment.id)).scalar() or 0
    recent_comments = db.query(func.count(Comment.id)).filter(
        Comment.published >= cutoff_date
    ).scalar() or 0
    
    # Top authors by posts
    top_authors_posts = db.query(
        User.username,
        User.name,
        func.count(BlogPost.id).label('post_count')
    ).join(BlogPost, User.id == BlogPost.author_id).group_by(
        User.id, User.username, User.name
    ).order_by(desc(func.count(BlogPost.id))).limit(5).all()
    
    # Top authors by comments
    top_authors_comments = db.query(
        User.username,
        User.name,
        func.count(Comment.id).label('comment_count')
    ).join(Comment, User.id == Comment.author_id).group_by(
        User.id, User.username, User.name
    ).order_by(desc(func.count(Comment.id))).limit(5).all()
    
    return {
        "total_posts": total_posts,
        "recent_posts": recent_posts,
        "total_comments": total_comments,
        "recent_comments": recent_comments,
        "top_authors_by_posts": [
            {"username": author.username, "name": author.name, "count": author.post_count}
            for author in top_authors_posts
        ],
        "top_authors_by_comments": [
            {"username": author.username, "name": author.name, "count": author.comment_count}
            for author in top_authors_comments
        ],
        "period_days": days
    }