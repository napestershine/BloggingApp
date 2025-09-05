# WhatsApp Notifications for BloggingApp

This feature allows users to receive WhatsApp notifications for repository events in the BloggingApp.

## Features

- ✅ **Blog Post Notifications**: Get notified when new blog posts are published
- ✅ **Comment Notifications**: Receive alerts when someone comments on your posts  
- ✅ **User Preferences**: Fine-grained control over notification types
- ✅ **Phone Number Validation**: International phone number format validation
- ✅ **Test Notifications**: Send test messages to verify setup

## Setup Instructions

### 1. Twilio WhatsApp Business API Setup

1. Sign up for a [Twilio account](https://www.twilio.com/)
2. Get approved for WhatsApp Business API (required for production)
3. Obtain your credentials:
   - Account SID
   - Auth Token  
   - WhatsApp-enabled phone number

### 2. Environment Configuration

Add the following environment variables to your `.env` file:

```bash
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=+1234567890
```

### 3. User Setup

Users need to configure their WhatsApp preferences:

1. Set their WhatsApp phone number (international format: +1234567890)
2. Enable WhatsApp notifications
3. Choose which types of notifications to receive

## API Endpoints

### Get WhatsApp Settings
```http
GET /notifications/whatsapp
Authorization: Bearer <jwt_token>
```

Response:
```json
{
  "whatsapp_number": "+1234567890",
  "whatsapp_notifications_enabled": true,
  "notify_on_new_posts": true,
  "notify_on_comments": true,
  "notify_on_mentions": true
}
```

### Update WhatsApp Settings
```http
PUT /notifications/whatsapp
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "whatsapp_number": "+1234567890",
  "whatsapp_notifications_enabled": true,
  "notify_on_new_posts": false,
  "notify_on_comments": true,
  "notify_on_mentions": true
}
```

### Send Test Notification
```http
POST /notifications/whatsapp/test
Authorization: Bearer <jwt_token>
```

## Notification Events

### New Blog Post
- **Trigger**: When a new blog post is created
- **Recipients**: Users who follow the author (future feature)
- **Content**: Blog post title and author name

### New Comment  
- **Trigger**: When someone comments on a blog post
- **Recipients**: Blog post author (if not the commenter)
- **Content**: Commenter name, post title, and comment preview

### Mentions (Future)
- **Trigger**: When a user is mentioned in a comment (@username)
- **Recipients**: The mentioned user
- **Content**: Who mentioned them and in which post

## Technical Implementation

### Database Schema Changes

Added to `User` model:
```sql
whatsapp_number VARCHAR(20) NULL,
whatsapp_notifications_enabled BOOLEAN DEFAULT FALSE,
notify_on_new_posts BOOLEAN DEFAULT TRUE,
notify_on_comments BOOLEAN DEFAULT TRUE,
notify_on_mentions BOOLEAN DEFAULT TRUE
```

### Service Architecture

- **NotificationService**: Handles WhatsApp message sending via Twilio API
- **Async Processing**: Notifications are sent asynchronously to avoid blocking main operations
- **Graceful Degradation**: Failed notifications don't impact core functionality

### Error Handling

- Invalid phone numbers are rejected with validation error
- Service gracefully handles Twilio API failures
- Notifications can be disabled without affecting other features

## Testing

Run the notification tests:
```bash
pytest app/tests/test_whatsapp_notifications.py -v
pytest app/tests/test_notification_endpoints.py -v
```

## Security Considerations

1. **Opt-in Only**: Users must explicitly enable notifications
2. **Phone Number Validation**: Format validation prevents invalid numbers
3. **Rate Limiting**: Consider implementing rate limits for production
4. **Credentials Security**: Store Twilio credentials securely in environment variables

## Production Deployment

1. **Twilio Approval**: Get WhatsApp Business API approved for production use
2. **Rate Limiting**: Implement notification rate limiting
3. **Monitoring**: Set up logging and monitoring for notification delivery
4. **Backup Strategy**: Consider fallback notification methods (email, in-app)

## Future Enhancements

- [ ] **User Following System**: Allow users to follow other users
- [ ] **Rich Message Templates**: Use WhatsApp message templates for better formatting  
- [ ] **Notification Scheduling**: Allow users to set quiet hours
- [ ] **Bulk Notifications**: Efficient delivery for popular posts
- [ ] **Analytics**: Track notification delivery and engagement
- [ ] **Multiple Providers**: Support other messaging platforms (Telegram, SMS)

## Troubleshooting

### Common Issues

1. **"WhatsApp service not enabled"**: Check Twilio credentials in `.env` file
2. **"Invalid phone number format"**: Use international format (+1234567890)
3. **Test notification fails**: Verify Twilio account has WhatsApp sandbox enabled
4. **Database errors**: Ensure database schema is updated with new columns

### Support

For issues related to:
- Twilio setup: Check [Twilio WhatsApp documentation](https://www.twilio.com/docs/whatsapp)
- Phone number formatting: Use [E.164 format](https://en.wikipedia.org/wiki/E.164)
- API endpoints: Check the interactive docs at `/docs` when running the application