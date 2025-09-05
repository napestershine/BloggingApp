from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.auth.auth import get_current_user
from app.models.models import User
from app.schemas.schemas import WhatsAppSettings, WhatsAppSettingsUpdate
import re

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)

def validate_phone_number(phone: str) -> bool:
    """Validate phone number format (basic validation)"""
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    # Should start with + and have 7-15 digits
    pattern = r'^\+\d{7,15}$'
    return bool(re.match(pattern, cleaned))

@router.get("/whatsapp", response_model=WhatsAppSettings)
async def get_whatsapp_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's WhatsApp notification settings"""
    return WhatsAppSettings(
        whatsapp_number=current_user.whatsapp_number,
        whatsapp_notifications_enabled=current_user.whatsapp_notifications_enabled or False,
        notify_on_new_posts=current_user.notify_on_new_posts if current_user.notify_on_new_posts is not None else True,
        notify_on_comments=current_user.notify_on_comments if current_user.notify_on_comments is not None else True,
        notify_on_mentions=current_user.notify_on_mentions if current_user.notify_on_mentions is not None else True
    )

@router.put("/whatsapp", response_model=WhatsAppSettings)
async def update_whatsapp_settings(
    settings_update: WhatsAppSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update WhatsApp notification settings for current user"""
    
    # Get the user from the database to ensure it's attached to the session
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Validate phone number if provided
    if settings_update.whatsapp_number is not None:
        if settings_update.whatsapp_number and not validate_phone_number(settings_update.whatsapp_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone number format. Use international format like +1234567890"
            )
        user.whatsapp_number = settings_update.whatsapp_number
    
    # Update settings if provided
    if settings_update.whatsapp_notifications_enabled is not None:
        user.whatsapp_notifications_enabled = settings_update.whatsapp_notifications_enabled
    
    if settings_update.notify_on_new_posts is not None:
        user.notify_on_new_posts = settings_update.notify_on_new_posts
        
    if settings_update.notify_on_comments is not None:
        user.notify_on_comments = settings_update.notify_on_comments
        
    if settings_update.notify_on_mentions is not None:
        user.notify_on_mentions = settings_update.notify_on_mentions
    
    db.commit()
    db.refresh(user)
    
    return WhatsAppSettings(
        whatsapp_number=user.whatsapp_number,
        whatsapp_notifications_enabled=user.whatsapp_notifications_enabled or False,
        notify_on_new_posts=user.notify_on_new_posts if user.notify_on_new_posts is not None else True,
        notify_on_comments=user.notify_on_comments if user.notify_on_comments is not None else True,
        notify_on_mentions=user.notify_on_mentions if user.notify_on_mentions is not None else True
    )

@router.post("/whatsapp/test")
async def test_whatsapp_notification(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a test WhatsApp notification to verify setup"""
    from app.services.notification_service import whatsapp_service
    
    if not current_user.whatsapp_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="WhatsApp number not configured. Please set your WhatsApp number first."
        )
    
    if not current_user.whatsapp_notifications_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="WhatsApp notifications are disabled. Please enable them first."
        )
    
    success = await whatsapp_service.send_whatsapp_message(
        current_user.whatsapp_number,
        f"🎉 Test notification from BloggingApp!\n\nHi {current_user.name}, your WhatsApp notifications are working perfectly!"
    )
    
    if success:
        return {"message": "Test notification sent successfully!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send test notification. Please check your WhatsApp number and service configuration."
        )