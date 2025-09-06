from typing import Optional
from sqlalchemy.orm import Session
from app.models.models import Notification, NotificationType, User, BlogPost, Comment
from app.database.connection import get_session_local
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for creating and managing notifications"""
    
    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        notification_type: NotificationType,
        title: str,
        message: str,
        related_user_id: Optional[int] = None,
        related_post_id: Optional[int] = None,
        related_comment_id: Optional[int] = None
    ) -> Notification:
        """
        Create a new notification
        
        Args:
            db: Database session
            user_id: ID of user to receive notification
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            related_user_id: ID of user who triggered the notification
            related_post_id: ID of related blog post
            related_comment_id: ID of related comment
            
        Returns:
            Created notification
        """
        
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            title=title,
            message=message,
            related_user_id=related_user_id,
            related_post_id=related_post_id,
            related_comment_id=related_comment_id
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        logger.info(f"Created notification for user {user_id}: {title}")
        return notification
    
    @staticmethod
    def create_follow_notification(
        db: Session,
        followed_user_id: int,
        follower_user: User
    ):
        """Create notification when a user is followed"""
        
        title = "New Follower"
        message = f"{follower_user.name} (@{follower_user.username}) started following you"
        
        return NotificationService.create_notification(
            db=db,
            user_id=followed_user_id,
            notification_type=NotificationType.FOLLOW,
            title=title,
            message=message,
            related_user_id=follower_user.id
        )
    
    @staticmethod
    def create_post_like_notification(
        db: Session,
        post: BlogPost,
        liker_user: User
    ):
        """Create notification when a post is liked"""
        
        # Don't notify if user likes their own post
        if post.author_id == liker_user.id:
            return None
            
        title = "Post Liked"
        message = f"{liker_user.name} liked your post \"{post.title[:50]}{'...' if len(post.title) > 50 else ''}\""
        
        return NotificationService.create_notification(
            db=db,
            user_id=post.author_id,
            notification_type=NotificationType.POST_LIKE,
            title=title,
            message=message,
            related_user_id=liker_user.id,
            related_post_id=post.id
        )
    
    @staticmethod
    def create_post_comment_notification(
        db: Session,
        post: BlogPost,
        comment: Comment,
        commenter_user: User
    ):
        """Create notification when a post is commented on"""
        
        # Don't notify if user comments on their own post
        if post.author_id == commenter_user.id:
            return None
            
        title = "New Comment"
        message = f"{commenter_user.name} commented on your post \"{post.title[:50]}{'...' if len(post.title) > 50 else ''}\""
        
        return NotificationService.create_notification(
            db=db,
            user_id=post.author_id,
            notification_type=NotificationType.POST_COMMENT,
            title=title,
            message=message,
            related_user_id=commenter_user.id,
            related_post_id=post.id,
            related_comment_id=comment.id
        )
    
    @staticmethod
    def create_comment_reply_notification(
        db: Session,
        parent_comment: Comment,
        reply_comment: Comment,
        replier_user: User
    ):
        """Create notification when a comment is replied to"""
        
        # Don't notify if user replies to their own comment
        if parent_comment.author_id == replier_user.id:
            return None
            
        title = "Comment Reply"
        message = f"{replier_user.name} replied to your comment"
        
        return NotificationService.create_notification(
            db=db,
            user_id=parent_comment.author_id,
            notification_type=NotificationType.COMMENT_REPLY,
            title=title,
            message=message,
            related_user_id=replier_user.id,
            related_post_id=parent_comment.blog_post_id,
            related_comment_id=reply_comment.id
        )

# Create a global instance
notification_service = NotificationService()