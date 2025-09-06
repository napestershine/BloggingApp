import logging
from typing import Optional
from datetime import datetime, timedelta
from collections import defaultdict
from twilio.rest import Client
from app.core.config import settings

logger = logging.getLogger(__name__)

class WhatsAppNotificationService:
    """Service for sending WhatsApp notifications using Twilio API with rate limiting"""
    
    def __init__(self):
        self.account_sid = settings.twilio_account_sid
        self.auth_token = settings.twilio_auth_token  
        self.whatsapp_number = settings.twilio_whatsapp_number
        self.client = None
        
        # Rate limiting tracking
        self.message_counts_per_minute = defaultdict(list)
        self.message_counts_per_hour = defaultdict(list)
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid.get_secret_value(), self.auth_token.get_secret_value())
        else:
            logger.warning("Twilio credentials not configured. WhatsApp notifications disabled.")
    
    def is_enabled(self) -> bool:
        """Check if WhatsApp notification service is properly configured"""
        return (self.client is not None and 
                self.whatsapp_number is not None and 
                settings.whatsapp_notifications_enabled)
    
    def _check_rate_limit(self, to_number: str) -> bool:
        """Check if sending to this number would exceed rate limits"""
        now = datetime.now()
        
        # Clean old entries
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        
        self.message_counts_per_minute[to_number] = [
            timestamp for timestamp in self.message_counts_per_minute[to_number]
            if timestamp > minute_ago
        ]
        self.message_counts_per_hour[to_number] = [
            timestamp for timestamp in self.message_counts_per_hour[to_number]
            if timestamp > hour_ago
        ]
        
        # Check limits
        minute_count = len(self.message_counts_per_minute[to_number])
        hour_count = len(self.message_counts_per_hour[to_number])
        
        if minute_count >= settings.whatsapp_rate_limit_per_minute:
            logger.warning(f"Rate limit exceeded for {to_number}: {minute_count} messages in last minute")
            return False
        
        if hour_count >= settings.whatsapp_rate_limit_per_hour:
            logger.warning(f"Rate limit exceeded for {to_number}: {hour_count} messages in last hour")
            return False
        
        return True
    
    def _record_message_sent(self, to_number: str):
        """Record that a message was sent for rate limiting"""
        now = datetime.now()
        self.message_counts_per_minute[to_number].append(now)
        self.message_counts_per_hour[to_number].append(now)
    
    async def send_whatsapp_message(self, to_number: str, message: str) -> bool:
        """
        Send a WhatsApp message to a phone number with rate limiting
        
        Args:
            to_number: Recipient's WhatsApp number (format: +1234567890)
            message: Message content to send
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        if not self.is_enabled():
            logger.warning("WhatsApp service not enabled. Skipping message.")
            return False
        
        # Check rate limits
        if not self._check_rate_limit(to_number):
            logger.warning(f"Rate limit exceeded for {to_number}. Message not sent.")
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
            
            # Record the message for rate limiting
            self._record_message_sent(to_number.replace('whatsapp:', ''))
            
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