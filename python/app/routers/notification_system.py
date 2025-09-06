from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from app.database.connection import get_db
from app.models.models import User, Notification, NotificationType, BlogPost, Comment
from app.schemas.schemas import (
    NotificationResponse,
    NotificationUpdate,
    NotificationStats,
    NotificationTypeEnum
)
from app.auth.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    skip: int = Query(0, ge=0, description="Number of notifications to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of notifications to return"),
    unread_only: bool = Query(False, description="Return only unread notifications"),
    type_filter: Optional[NotificationTypeEnum] = Query(None, description="Filter by notification type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user notifications
    
    - **skip**: Number of notifications to skip (pagination)
    - **limit**: Number of notifications to return (max 100)
    - **unread_only**: If true, only return unread notifications
    - **type_filter**: Filter notifications by type
    
    Returns list of notifications for the current user
    """
    
    # Start with base query for current user's notifications
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    # Apply filters
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    if type_filter:
        query = query.filter(Notification.type == NotificationType(type_filter.value))
    
    # Order by newest first
    query = query.order_by(Notification.created_at.desc())
    
    # Apply pagination
    notifications = query.offset(skip).limit(limit).all()
    
    # Format notifications with related data
    result = []
    for notif in notifications:
        notif_dict = {
            "id": notif.id,
            "user_id": notif.user_id,
            "type": notif.type.value,
            "title": notif.title,
            "message": notif.message,
            "is_read": notif.is_read,
            "created_at": notif.created_at,
            "read_at": notif.read_at,
            "related_user_id": notif.related_user_id,
            "related_post_id": notif.related_post_id,
            "related_comment_id": notif.related_comment_id,
            "related_user": None,
            "related_post": None
        }
        
        # Add related user info if available
        if notif.related_user_id:
            related_user = db.query(User).filter(User.id == notif.related_user_id).first()
            if related_user:
                notif_dict["related_user"] = {
                    "id": related_user.id,
                    "username": related_user.username,
                    "name": related_user.name,
                    "bio": related_user.bio,
                    "avatar_url": related_user.avatar_url,
                    "created_at": related_user.created_at
                }
        
        # Add related post info if available
        if notif.related_post_id:
            related_post = db.query(BlogPost).filter(BlogPost.id == notif.related_post_id).first()
            if related_post:
                notif_dict["related_post"] = {
                    "id": related_post.id,
                    "title": related_post.title,
                    "slug": related_post.slug
                }
        
        result.append(notif_dict)
    
    return result

@router.get("/stats", response_model=NotificationStats)
def get_notification_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get notification statistics for the current user
    
    Returns total count and unread count of notifications
    """
    
    # Count total notifications
    total_count = db.query(func.count(Notification.id)).filter(
        Notification.user_id == current_user.id
    ).scalar()
    
    # Count unread notifications
    unread_count = db.query(func.count(Notification.id)).filter(
        and_(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
    ).scalar()
    
    return NotificationStats(
        total_count=total_count,
        unread_count=unread_count
    )

@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(
    notification_id: int,
    notification_update: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a notification (mainly to mark as read/unread)
    
    - **notification_id**: ID of the notification to update
    - **is_read**: Whether the notification is read
    
    Returns the updated notification
    """
    
    # Find the notification
    notification = db.query(Notification).filter(
        and_(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    # Update fields
    if notification_update.is_read is not None:
        notification.is_read = notification_update.is_read
        if notification_update.is_read:
            notification.read_at = func.now()
        else:
            notification.read_at = None
    
    db.commit()
    db.refresh(notification)
    
    # Return formatted notification
    return {
        "id": notification.id,
        "user_id": notification.user_id,
        "type": notification.type.value,
        "title": notification.title,
        "message": notification.message,
        "is_read": notification.is_read,
        "created_at": notification.created_at,
        "read_at": notification.read_at,
        "related_user_id": notification.related_user_id,
        "related_post_id": notification.related_post_id,
        "related_comment_id": notification.related_comment_id,
        "related_user": None,
        "related_post": None
    }

@router.put("/mark-all-read")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark all notifications as read for the current user
    
    Returns the number of notifications marked as read
    """
    
    # Update all unread notifications
    updated_count = db.query(Notification).filter(
        and_(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
    ).update({
        "is_read": True,
        "read_at": func.now()
    })
    
    db.commit()
    
    return {"message": f"Marked {updated_count} notifications as read"}

@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a notification
    
    - **notification_id**: ID of the notification to delete
    
    Returns success message
    """
    
    # Find the notification
    notification = db.query(Notification).filter(
        and_(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    db.delete(notification)
    db.commit()
    
    return {"message": "Notification deleted successfully"}

@router.delete("/")
def delete_all_notifications(
    read_only: bool = Query(False, description="If true, only delete read notifications"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete notifications for the current user
    
    - **read_only**: If true, only delete read notifications; if false, delete all
    
    Returns the number of notifications deleted
    """
    
    # Build query
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if read_only:
        query = query.filter(Notification.is_read == True)
    
    # Count notifications to be deleted
    delete_count = query.count()
    
    # Delete notifications
    query.delete()
    db.commit()
    
    return {"message": f"Deleted {delete_count} notifications"}