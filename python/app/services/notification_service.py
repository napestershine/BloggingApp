import logging
from typing import Optional
from twilio.rest import Client
from app.core.config import settings

logger = logging.getLogger(__name__)

class WhatsAppNotificationService:
    """Service for sending WhatsApp notifications using Twilio API"""
    
    def __init__(self):
        self.account_sid = settings.twilio_account_sid
        self.auth_token = settings.twilio_auth_token  
        self.whatsapp_number = settings.twilio_whatsapp_number
        self.client = None
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            logger.warning("Twilio credentials not configured. WhatsApp notifications disabled.")
    
    def is_enabled(self) -> bool:
        """Check if WhatsApp notification service is properly configured"""
        return self.client is not None and self.whatsapp_number is not None
    
    async def send_whatsapp_message(self, to_number: str, message: str) -> bool:
        """
        Send a WhatsApp message to a phone number
        
        Args:
            to_number: Recipient's WhatsApp number (format: +1234567890)
            message: Message content to send
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        if not self.is_enabled():
            logger.warning("WhatsApp service not enabled. Skipping message.")
            return False
            
        try:
            # Ensure phone number has proper WhatsApp prefix
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            from_number = f'whatsapp:{self.whatsapp_number}'
            
            message = self.client.messages.create(
                body=message,
                from_=from_number,
                to=to_number
            )
            
            logger.info(f"WhatsApp message sent successfully. SID: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {str(e)}")
            return False
    
    async def notify_new_blog_post(self, author_name: str, post_title: str, to_number: str) -> bool:
        """Send notification for new blog post"""
        message = f"📝 New blog post by {author_name}:\n\n'{post_title}'\n\nCheck it out on the BloggingApp!"
        return await self.send_whatsapp_message(to_number, message)
    
    async def notify_new_comment(self, commenter_name: str, post_title: str, comment_preview: str, to_number: str) -> bool:
        """Send notification for new comment on user's post"""
        preview = comment_preview[:100] + "..." if len(comment_preview) > 100 else comment_preview
        message = f"💬 New comment on your post '{post_title}' by {commenter_name}:\n\n{preview}\n\nReply on BloggingApp!"
        return await self.send_whatsapp_message(to_number, message)
    
    async def notify_mention(self, mentioned_by: str, post_title: str, to_number: str) -> bool:
        """Send notification when user is mentioned in a comment"""
        message = f"👋 You were mentioned by {mentioned_by} in '{post_title}'\n\nSee what they said on BloggingApp!"
        return await self.send_whatsapp_message(to_number, message)

# Global instance
whatsapp_service = WhatsAppNotificationService()