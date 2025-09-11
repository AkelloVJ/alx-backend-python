# Pagination and Filtering Implementation

This document describes the implementation of pagination and filtering functionality for the Django messaging app.

## Overview

The implementation includes:
- **Pagination**: 20 messages per page with customizable page sizes
- **Filtering**: Advanced filtering using django-filter for messages, conversations, and users
- **Search**: Full-text search across message content and user information
- **Ordering**: Flexible ordering options for all endpoints

## Implementation Details

### 1. Pagination Configuration

**File**: `messaging_app/settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'chats.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

### 2. Custom Pagination Classes

**File**: `chats/pagination.py`

- **StandardResultsSetPagination**: Default pagination (20 items per page)
- **MessagePagination**: Enhanced pagination for messages with conversation context
- **ConversationPagination**: Pagination for conversations (10 items per page)
- **UserPagination**: Pagination for users (15 items per page)

### 3. Filter Classes

**File**: `chats/filters.py`

#### MessageFilter
- **Sender filtering**: `sender`, `sender_email`, `sender_name`
- **Conversation filtering**: `conversation`, `participant`, `participant_email`
- **Time range filtering**: `sent_after`, `sent_before`, `sent_date`, `sent_date_range`
- **Content filtering**: `message_contains`, `message_exact`, `message_startswith`
- **Ordering**: Multiple ordering options with field labels

#### ConversationFilter
- **Participant filtering**: `participant`, `participant_email`, `participant_name`
- **Time filtering**: `created_after`, `created_before`, `created_date`, `created_date_range`
- **Ordering**: Creation date and participant name ordering

#### UserFilter
- **Name filtering**: `first_name`, `last_name`, `full_name`
- **Contact filtering**: `email`, `phone_number`
- **Role filtering**: `role`
- **Time filtering**: `created_after`, `created_before`, `created_date`, `created_date_range`
- **Ordering**: Multiple field ordering options

### 4. ViewSet Updates

**File**: `chats/views.py`

All ViewSets now include:
- Custom pagination classes
- Filter backends (DjangoFilterBackend, SearchFilter, OrderingFilter)
- Filter set classes
- Search fields
- Ordering fields and default ordering

## API Usage Examples

### Pagination

#### Basic Pagination
```bash
GET /api/messages/
# Returns first 20 messages with pagination metadata
```

#### Page Navigation
```bash
GET /api/messages/?page=2
# Returns page 2 of messages
```

#### Custom Page Size
```bash
GET /api/messages/?page_size=10
# Returns 10 messages per page
```

### Filtering

#### Filter by Sender
```bash
GET /api/messages/?sender=USER_UUID
# Filter messages by specific sender
```

#### Filter by Message Content
```bash
GET /api/messages/?message_contains=work
# Filter messages containing "work"
```

#### Filter by Date Range
```bash
GET /api/messages/?sent_after=2024-01-01T00:00:00Z&sent_before=2024-01-31T23:59:59Z
# Filter messages within date range
```

#### Filter by Date
```bash
GET /api/messages/?sent_date=2024-01-15
# Filter messages from specific date
```

#### Filter by Conversation
```bash
GET /api/messages/?conversation=CONVERSATION_UUID
# Filter messages from specific conversation
```

### Ordering

#### Order by Sent Date
```bash
GET /api/messages/?ordering=sent_at
# Order by sent date (ascending)

GET /api/messages/?ordering=-sent_at
# Order by sent date (descending)
```

#### Order by Sender Name
```bash
GET /api/messages/?ordering=sender__first_name
# Order by sender first name (ascending)
```

### Search

#### Search in Messages
```bash
GET /api/messages/?search=important
# Search for "important" in message content and sender info
```

### Combined Filtering

#### Complex Query
```bash
GET /api/messages/?message_contains=work&sent_after=2024-01-01&ordering=-sent_at&page=1&page_size=10
# Complex filtering with pagination and ordering
```

## Custom Actions

### Recent Messages
```bash
GET /api/messages/recent/?limit=10
# Get recent messages (limited to 10)
```

### Messages by Sender
```bash
GET /api/messages/by_sender/?sender_id=USER_UUID
# Get messages from specific sender
```

### Messages by Date Range
```bash
GET /api/messages/by_date_range/?start_date=2024-01-01&end_date=2024-01-31
# Get messages within date range
```

### Search Messages
```bash
GET /api/messages/search/?q=query
# Search messages by content
```

## Response Format

### Paginated Response
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/messages/?page=2",
    "previous": null,
    "page_size": 20,
    "current_page": 1,
    "total_pages": 5,
    "has_next": true,
    "has_previous": false,
    "results": [
        {
            "message_id": "uuid",
            "sender": "uuid",
            "conversation": "uuid",
            "message_body": "Message content",
            "sent_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

## Filter Parameters Reference

### Message Filters
| Parameter | Type | Description |
|-----------|------|-------------|
| `sender` | UUID | Filter by sender user ID |
| `sender_email` | String | Filter by sender email (contains) |
| `sender_name` | String | Filter by sender first name (contains) |
| `conversation` | UUID | Filter by conversation ID |
| `participant` | UUID | Filter by conversation participant |
| `sent_after` | DateTime | Filter messages after date |
| `sent_before` | DateTime | Filter messages before date |
| `sent_date` | Date | Filter messages on specific date |
| `sent_date_range` | DateRange | Filter messages within date range |
| `message_contains` | String | Filter by message content (contains) |
| `message_exact` | String | Filter by exact message content |
| `message_startswith` | String | Filter by message content (starts with) |

### Ordering Options
| Field | Description |
|-------|-------------|
| `sent_at` | Sent date (oldest first) |
| `-sent_at` | Sent date (newest first) |
| `sender__first_name` | Sender name (A-Z) |
| `-sender__first_name` | Sender name (Z-A) |
| `message_body` | Message content (A-Z) |
| `-message_body` | Message content (Z-A) |

### Search Fields
- `message_body` - Message content
- `sender__first_name` - Sender first name
- `sender__last_name` - Sender last name
- `sender__email` - Sender email

## Performance Considerations

1. **Database Indexes**: Ensure proper indexes on frequently filtered fields
2. **Page Size Limits**: Maximum page size is 100 to prevent performance issues
3. **Query Optimization**: Use select_related and prefetch_related for related objects
4. **Caching**: Consider implementing caching for frequently accessed data

## Testing

Run the comprehensive test script:

```bash
cd /home/victor/Desktop/Airbnb/alx-backend-python/messaging_app
python test_pagination_filtering.py
```

The test script covers:
- Basic pagination
- Page navigation
- Custom page sizes
- All filter types
- Ordering options
- Search functionality
- Combined filtering
- Custom actions

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Start Server**:
   ```bash
   python manage.py runserver
   ```

## Dependencies Added

- `django-filter==24.3` - Advanced filtering capabilities
- `rest_framework` - Built-in pagination and filtering support

## Files Modified/Created

1. **`requirements.txt`** - Added django-filter dependency
2. **`messaging_app/settings.py`** - Added pagination and filter configuration
3. **`chats/pagination.py`** - Created custom pagination classes
4. **`chats/filters.py`** - Created filter classes for all models
5. **`chats/views.py`** - Updated ViewSets with pagination and filtering
6. **`test_pagination_filtering.py`** - Created comprehensive test script
7. **`PAGINATION_FILTERING_README.md`** - Created documentation

The implementation provides a robust, scalable solution for pagination and filtering that enhances the user experience and API performance.
