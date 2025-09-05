from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from app.database.connection import get_db
from app.models.models import User, UserRole, BlogPost, Comment
from app.schemas.schemas import User as UserSchema
from app.admin.auth import require_admin_role, require_super_admin
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])

# User management schemas
class UserRoleUpdate(BaseModel):
    role: UserRole

class UserManagementResponse(BaseModel):
    id: int
    username: str
    email: str
    name: str
    role: UserRole
    created_at: datetime
    email_verified: bool
    total_posts: int
    total_comments: int

class AdminStats(BaseModel):
    total_users: int
    total_posts: int
    total_comments: int
    admin_users: int
    new_users_today: int
    new_posts_today: int
    new_comments_today: int

@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_role())
):
    """
    Get admin dashboard statistics
    """
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())
    
    # Get basic counts
    total_users = db.query(func.count(User.id)).scalar()
    total_posts = db.query(func.count(BlogPost.id)).scalar()
    total_comments = db.query(func.count(Comment.id)).scalar()
    admin_users = db.query(func.count(User.id)).filter(
        User.role.in_([UserRole.ADMIN, UserRole.SUPER_ADMIN])
    ).scalar()
    
    # Get today's new records
    new_users_today = db.query(func.count(User.id)).filter(
        User.created_at >= today_start
    ).scalar()
    new_posts_today = db.query(func.count(BlogPost.id)).filter(
        BlogPost.published >= today_start
    ).scalar()
    new_comments_today = db.query(func.count(Comment.id)).filter(
        Comment.published >= today_start
    ).scalar()
    
    return AdminStats(
        total_users=total_users or 0,
        total_posts=total_posts or 0,
        total_comments=total_comments or 0,
        admin_users=admin_users or 0,
        new_users_today=new_users_today or 0,
        new_posts_today=new_posts_today or 0,
        new_comments_today=new_comments_today or 0
    )

@router.get("/users", response_model=List[UserManagementResponse])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    role_filter: Optional[UserRole] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_role())
):
    """
    Get all users with pagination and filtering
    """
    query = db.query(User)
    
    # Apply role filter
    if role_filter:
        query = query.filter(User.role == role_filter)
    
    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                User.username.ilike(search_term),
                User.email.ilike(search_term),
                User.name.ilike(search_term)
            )
        )
    
    users = query.offset(skip).limit(limit).all()
    
    # Get post and comment counts for each user
    result = []
    for user in users:
        post_count = db.query(func.count(BlogPost.id)).filter(
            BlogPost.author_id == user.id
        ).scalar() or 0
        comment_count = db.query(func.count(Comment.id)).filter(
            Comment.author_id == user.id
        ).scalar() or 0
        
        result.append(UserManagementResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            name=user.name,
            role=user.role,
            created_at=user.created_at,
            email_verified=user.email_verified,
            total_posts=post_count,
            total_comments=comment_count
        ))
    
    return result

@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    role_update: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin())
):
    """
    Update user role (super admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent super admin from demoting themselves
    if user.id == current_user.id and role_update.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own super admin role"
        )
    
    user.role = role_update.role
    db.commit()
    db.refresh(user)
    
    return {"message": f"User role updated to {role_update.role.value}"}

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin())
):
    """
    Delete user (super admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent super admin from deleting themselves
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Delete user's posts and comments first (cascade)
    db.query(Comment).filter(Comment.author_id == user_id).delete()
    db.query(BlogPost).filter(BlogPost.author_id == user_id).delete()
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}

@router.get("/users/{user_id}", response_model=UserManagementResponse)
async def get_user_details(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_role())
):
    """
    Get detailed user information
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    post_count = db.query(func.count(BlogPost.id)).filter(
        BlogPost.author_id == user.id
    ).scalar() or 0
    comment_count = db.query(func.count(Comment.id)).filter(
        Comment.author_id == user.id
    ).scalar() or 0
    
    return UserManagementResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        name=user.name,
        role=user.role,
        created_at=user.created_at,
        email_verified=user.email_verified,
        total_posts=post_count,
        total_comments=comment_count
    )