# Django Signals and ORM Messaging App

A comprehensive Django messaging application implementing advanced ORM techniques, signals, and caching.

## Features Implemented

### 1. User Notifications with Signals
- **Message Model**: Complete message system with sender, receiver, content, timestamp, edited, read, and parent_message fields
- **Notification Model**: Automatic notifications when new messages are received
- **Post-save Signal**: Automatically creates notifications for message receivers

### 2. Message Edit History with Signals
- **MessageHistory Model**: Tracks all message edits with old content and edit timestamp
- **Pre-save Signal**: Logs old content before message updates
- **Edit Tracking**: Messages marked as edited when content changes

### 3. User Data Cleanup with Signals
- **Post-delete Signal**: Automatically cleans up all user-related data when account is deleted
- **Cascade Cleanup**: Removes messages, notifications, message history, and conversation data
- **Foreign Key Handling**: Proper cleanup respecting database constraints

### 4. Threaded Conversations with Advanced ORM
- **Self-referential Foreign Key**: Messages can have parent messages for threading
- **Recursive Queries**: Efficient retrieval of all replies in a thread
- **Optimized Queries**: Uses select_related and prefetch_related for performance

### 5. Custom ORM Manager for Unread Messages
- **UnreadMessagesManager**: Custom manager with specialized methods
- **Unread Filtering**: `for_user()` and `unread_count()` methods
- **Query Optimization**: Uses `.only()` to retrieve only necessary fields

### 6. View Caching
- **LocMemCache**: Configured with unique-snowflake location
- **Cache Decorator**: 60-second cache on conversation messages view
- **Performance**: Reduces database queries for frequently accessed data

## Project Structure

```
Django-signals_orm-0x04/
├── messaging/
│   ├── models.py          # All models with custom manager
│   ├── signals.py         # All signal handlers
│   ├── views.py           # API views with caching
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # URL patterns
│   ├── admin.py           # Admin interface
│   ├── apps.py            # App config with signal registration
│   └── tests.py           # Comprehensive test suite
├── messaging_app/
│   ├── settings.py        # Django settings with cache config
│   └── urls.py            # Main URL configuration
└── manage.py
```

## Models

### Message Model
```python
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages')
    receiver = models.ForeignKey(User, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies')
    
    objects = models.Manager()
    unread = UnreadMessagesManager()  # Custom manager
```

### Notification Model
```python
class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications')
    message = models.ForeignKey(Message, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
```

### MessageHistory Model
```python
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='edit_history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User)
```

## Signals

### 1. Message Notification Signal
```python
@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
```

### 2. Message Edit History Signal
```python
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Only for existing messages
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content,
                edited_by=instance.sender
            )
            instance.edited = True
```

### 3. User Deletion Cleanup Signal
```python
@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
    # ... additional cleanup
```

## API Endpoints

### Message Operations
- `POST /api/messages/send/` - Send a new message
- `PUT /api/messages/{id}/edit/` - Edit a message
- `POST /api/messages/{id}/read/` - Mark message as read
- `GET /api/messages/{id}/thread/` - Get message thread
- `GET /api/messages/{id}/history/` - Get edit history
- `GET /api/messages/unread/` - Get unread messages

### Conversation Operations
- `GET /api/conversations/` - List user conversations
- `GET /api/conversations/{id}/messages/` - Get conversation messages (cached)

### Notification Operations
- `GET /api/notifications/` - Get user notifications
- `POST /api/notifications/{id}/read/` - Mark notification as read

### User Management
- `DELETE /api/user/delete/` - Delete user account

## Caching Configuration

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

@cache_page(60)  # 60-second cache
def conversation_messages(request, conversation_id):
    # Cached view implementation
```

## Custom Manager Usage

```python
# Get unread messages for a user
unread_messages = Message.unread.for_user(user)

# Get unread count
count = Message.unread.unread_count(user)

# Optimized query with only necessary fields
messages = Message.unread.for_user(user).only(
    'id', 'content', 'timestamp', 'sender__username'
)
```

## Threaded Conversations

```python
# Get all replies to a message
def get_all_replies(self):
    replies = []
    direct_replies = self.replies.all().order_by('timestamp')
    
    for reply in direct_replies:
        replies.append(reply)
        replies.extend(reply.get_all_replies())  # Recursive
    
    return replies
```

## Testing

Run the comprehensive test suite:
```bash
python manage.py test messaging
```

Tests cover:
- Model creation and relationships
- Signal functionality
- API endpoints
- Caching behavior
- User deletion cleanup
- Threaded conversations
- Custom manager functionality

## Installation and Setup

1. **Activate virtual environment**:
   ```bash
   source ../venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install djangorestframework
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run server**:
   ```bash
   python manage.py runserver
   ```

6. **Access admin interface**:
   - URL: http://127.0.0.1:8000/admin/
   - Login with superuser credentials

## Key Features Demonstrated

1. **Django Signals**: Post-save, pre-save, and post-delete signals
2. **Advanced ORM**: Custom managers, select_related, prefetch_related
3. **Threaded Conversations**: Self-referential foreign keys and recursive queries
4. **Caching**: LocMemCache with cache_page decorator
5. **Data Cleanup**: Automatic cleanup on user deletion
6. **Performance Optimization**: Database query optimization techniques
7. **REST API**: Complete API with DRF serializers
8. **Testing**: Comprehensive test coverage

This implementation demonstrates advanced Django patterns and best practices for building scalable messaging applications.
