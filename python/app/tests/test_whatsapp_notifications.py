import pytest
from unittest.mock import patch, MagicMock
from app.services.notification_service import WhatsAppNotificationService

class TestWhatsAppNotificationService:
    """Test cases for WhatsApp notification service"""
    
    def test_is_enabled_with_valid_config(self):
        """Test that service is enabled when properly configured"""
        with patch('app.services.notification_service.settings') as mock_settings:
            mock_settings.twilio_account_sid = "test_sid"
            mock_settings.twilio_auth_token = "test_token"
            mock_settings.twilio_whatsapp_number = "+1234567890"
            
            with patch('app.services.notification_service.Client'):
                service = WhatsAppNotificationService()
                assert service.is_enabled() is True
    
    def test_is_enabled_with_missing_config(self):
        """Test that service is disabled when config is missing"""
        with patch('app.services.notification_service.settings') as mock_settings:
            mock_settings.twilio_account_sid = None
            mock_settings.twilio_auth_token = None
            mock_settings.twilio_whatsapp_number = None
            
            service = WhatsAppNotificationService()
            assert service.is_enabled() is False
    
    @pytest.mark.asyncio
    async def test_send_whatsapp_message_success(self):
        """Test successful WhatsApp message sending"""
        with patch('app.services.notification_service.settings') as mock_settings:
            mock_settings.twilio_account_sid = "test_sid"
            mock_settings.twilio_auth_token = "test_token"
            mock_settings.twilio_whatsapp_number = "+1234567890"
            
            mock_client = MagicMock()
            mock_message = MagicMock()
            mock_message.sid = "test_message_sid"
            mock_client.messages.create.return_value = mock_message
            
            with patch('app.services.notification_service.Client', return_value=mock_client):
                service = WhatsAppNotificationService()
                result = await service.send_whatsapp_message("+1987654321", "Test message")
                
                assert result is True
                mock_client.messages.create.assert_called_once_with(
                    body="Test message",
                    from_="whatsapp:+1234567890",
                    to="whatsapp:+1987654321"
                )
    
    @pytest.mark.asyncio
    async def test_send_whatsapp_message_service_disabled(self):
        """Test message sending when service is disabled"""
        with patch('app.services.notification_service.settings') as mock_settings:
            mock_settings.twilio_account_sid = None
            mock_settings.twilio_auth_token = None
            mock_settings.twilio_whatsapp_number = None
            
            service = WhatsAppNotificationService()
            result = await service.send_whatsapp_message("+1987654321", "Test message")
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_notify_new_blog_post(self):
        """Test blog post notification"""
        with patch('app.services.notification_service.settings') as mock_settings:
            mock_settings.twilio_account_sid = "test_sid"
            mock_settings.twilio_auth_token = "test_token"
            mock_settings.twilio_whatsapp_number = "+1234567890"
            
            mock_client = MagicMock()
            mock_message = MagicMock()
            mock_message.sid = "test_message_sid"
            mock_client.messages.create.return_value = mock_message
            
            with patch('app.services.notification_service.Client', return_value=mock_client):
                service = WhatsAppNotificationService()
                result = await service.notify_new_blog_post(
                    "John Doe", 
                    "My Amazing Blog Post", 
                    "+1987654321"
                )
                
                assert result is True
                mock_client.messages.create.assert_called_once()
                
                # Check that the message contains the expected content
                call_args = mock_client.messages.create.call_args[1]
                assert "John Doe" in call_args["body"]
                assert "My Amazing Blog Post" in call_args["body"]
    
    @pytest.mark.asyncio
    async def test_notify_new_comment(self):
        """Test comment notification"""
        with patch('app.services.notification_service.settings') as mock_settings:
            mock_settings.twilio_account_sid = "test_sid"
            mock_settings.twilio_auth_token = "test_token"
            mock_settings.twilio_whatsapp_number = "+1234567890"
            
            mock_client = MagicMock()
            mock_message = MagicMock()
            mock_message.sid = "test_message_sid"
            mock_client.messages.create.return_value = mock_message
            
            with patch('app.services.notification_service.Client', return_value=mock_client):
                service = WhatsAppNotificationService()
                result = await service.notify_new_comment(
                    "Jane Smith",
                    "Blog Post Title", 
                    "This is a great comment!",
                    "+1987654321"
                )
                
                assert result is True
                mock_client.messages.create.assert_called_once()
                
                # Check that the message contains the expected content
                call_args = mock_client.messages.create.call_args[1]
                assert "Jane Smith" in call_args["body"]
                assert "Blog Post Title" in call_args["body"]
                assert "This is a great comment!" in call_args["body"]