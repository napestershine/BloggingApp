from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from app.database.connection import get_db
from app.models.models import User, Notification, NotificationType, BlogPost, Comment
from app.schemas.schemas import (
    NotificationResponse,
    NotificationUpdate,
    NotificationStats,
    NotificationTypeEnum,
    FollowerUser
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
    Get user notifications with eager loading to prevent N+1 queries.
    
    - **skip**: Number of notifications to skip (pagination)
    - **limit**: Number of notifications to return (max 100)
    - **unread_only**: If true, only return unread notifications
    - **type_filter**: Filter notifications by type
    
    Returns list of notifications for the current user (O(1-2) queries)
    """
    
    # Start with base query for current user's notifications with eager loading
    query = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).options(
        joinedload(Notification.related_user),
        joinedload(Notification.related_post)
    )
    
    # Apply filters using .is_() for boolean comparisons (SQLAlchemy best practice)
    if unread_only:
        query = query.filter(Notification.is_read.is_(False))
    
    if type_filter:
        query = query.filter(Notification.type == NotificationType(type_filter.value))
    
    # Order by newest first
    query = query.order_by(Notification.created_at.desc())
    
    # Apply pagination
    notifications = query.offset(skip).limit(limit).all()
    
    # Build response with proper Pydantic models
    result = []
    for notif in notifications:
        # Build related user object if available
        related_user_obj = None
        if notif.related_user_id and notif.related_user:
            related_user_obj = FollowerUser(
                id=notif.related_user.id,
                username=notif.related_user.username,
                name=notif.related_user.name,
                bio=notif.related_user.bio,
                avatar_url=notif.related_user.avatar_url,
                created_at=notif.related_user.created_at,
            )
        
        # Build related post dict if available
        related_post = None
        if notif.related_post_id and notif.related_post:
            related_post = {
                "id": notif.related_post.id,
                "title": notif.related_post.title,
                "slug": notif.related_post.slug
            }
        
        # Create Pydantic model response
        notif_response = NotificationResponse(
            id=notif.id,
            user_id=notif.user_id,
            type=NotificationTypeEnum(notif.type.value),
            title=notif.title,
            message=notif.message,
            is_read=notif.is_read,
            created_at=notif.created_at,
            read_at=notif.read_at,
            related_user_id=notif.related_user_id,
            related_post_id=notif.related_post_id,
            related_comment_id=notif.related_comment_id,
            related_user=related_user_obj,
            related_post=related_post
        )
        
        result.append(notif_response)
    
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
    
    # Count unread notifications using .is_() for proper boolean filtering
    unread_count = db.query(func.count(Notification.id)).filter(
        and_(
            Notification.user_id == current_user.id,
            Notification.is_read.is_(False)
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
    
    Returns the updated notification as Pydantic model
    """
    
    # Find the notification with eager loading
    notification = db.query(Notification).options(
        joinedload(Notification.related_user),
        joinedload(Notification.related_post)
    ).filter(
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
    
    # Build response with Pydantic model
    related_user_obj = None
    if notification.related_user_id and notification.related_user:
        related_user_obj = FollowerUser(
            id=notification.related_user.id,
            username=notification.related_user.username,
            name=notification.related_user.name,
            bio=notification.related_user.bio,
            avatar_url=notification.related_user.avatar_url,
            created_at=notification.related_user.created_at,
        )
    
    related_post = None
    if notification.related_post_id and notification.related_post:
        related_post = {
            "id": notification.related_post.id,
            "title": notification.related_post.title,
            "slug": notification.related_post.slug
        }
    
    return NotificationResponse(
        id=notification.id,
        user_id=notification.user_id,
        type=NotificationTypeEnum(notification.type.value),
        title=notification.title,
        message=notification.message,
        is_read=notification.is_read,
        created_at=notification.created_at,
        read_at=notification.read_at,
        related_user_id=notification.related_user_id,
        related_post_id=notification.related_post_id,
        related_comment_id=notification.related_comment_id,
        related_user=related_user_obj,
        related_post=related_post
    )

@router.patch("/read-all")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark all unread notifications as read for the current user.
    
    Returns the number of notifications marked as read.
    """
    
    # Update all unread notifications for current user
    # Use synchronize_session=False for better performance on bulk operations
    updated_count = db.query(Notification).filter(
        and_(
            Notification.user_id == current_user.id,
            Notification.is_read.is_(False)
        )
    ).update(
        {
            Notification.is_read: True,
            Notification.read_at: func.now()
        },
        synchronize_session=False
    )
    
    db.commit()
    
    return {"message": f"Marked {updated_count} notifications as read", "count": updated_count}

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
    limit: int = Query(None, ge=1, le=1000, description="Maximum number of notifications to delete (default: all, max: 1000)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete notifications for the current user with safety guardrails.
    
    - **read_only**: If true, only delete read notifications; if false, delete all
    - **limit**: Maximum number of notifications to delete (capped at 1000 for safety)
    
    Returns the number of notifications deleted.
    """
    
    # Build query scoped to current user
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if read_only:
        query = query.filter(Notification.is_read.is_(True))
    
    # `Query.delete()` does not support `limit()`, so materialize the capped ID set first.
    notification_ids = None
    if limit:
        notification_ids = [
            notification_id
            for (notification_id,) in query.with_entities(Notification.id)
            .order_by(Notification.id)
            .limit(limit)
            .all()
        ]
        delete_count = len(notification_ids)
    else:
        delete_count = query.count()
    
    # Log bulk operation for safety/auditing
    logger.info(f"User {current_user.id} deleting {delete_count} notification(s)")
    
    # Delete notifications with proper session synchronization
    if delete_count:
        delete_query = query
        if notification_ids is not None:
            delete_query = db.query(Notification).filter(Notification.id.in_(notification_ids))
        delete_query.delete(synchronize_session=False)
    db.commit()
    
    return {
        "message": f"Deleted {delete_count} notification(s)",
        "count": delete_count
    }
