# Custom Permission Classes Implementation

This document describes the implementation of custom permission classes for the Django messaging app, specifically the `IsParticipantOfConversation` permission class.

## Overview

The `IsParticipantOfConversation` permission class has been created and implemented to enforce strict access control:

1. **Authentication Required**: Only authenticated users can access the API
2. **Conversation Participation**: Only participants in a conversation can send, view, update, and delete messages

## Implementation Details

### 1. Custom Permission Class

**File**: `chats/permissions.py`

```python
class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission class that:
    - Allows only authenticated users to access the API
    - Allows only participants in a conversation to send, view, update and delete messages
    """
    
    def has_permission(self, request, view):
        """
        Check if the user is authenticated
        """
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant in the conversation
        """
        # For conversation objects, check if user is a participant
        if hasattr(obj, 'participants_id'):
            return obj.participants_id == request.user
        
        # For message objects, check if user is a participant in the conversation
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants_id == request.user
        
        # For other objects, deny access by default
        return False
```

### 2. ViewSet Updates

**File**: `chats/views.py`

Both `ConversationViewSet` and `MessageViewSet` now use the custom permission:

```python
class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations
    """
    permission_classes = [IsParticipantOfConversation]

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages
    """
    permission_classes = [IsParticipantOfConversation]
```

### 3. Global Permission Setting

**File**: `messaging_app/settings.py`

The custom permission is set as the default permission class globally:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'chats.permissions.IsParticipantOfConversation',
    ],
}
```

## Permission Logic

### Authentication Check (`has_permission`)

- **Purpose**: Ensures only authenticated users can access any API endpoint
- **Implementation**: Returns `request.user.is_authenticated`
- **Result**: Unauthenticated requests receive HTTP 401 Unauthorized

### Object Permission Check (`has_object_permission`)

- **Purpose**: Ensures users can only access conversations they participate in
- **For Conversation Objects**: Checks if `obj.participants_id == request.user`
- **For Message Objects**: Checks if `obj.conversation.participants_id == request.user`
- **Result**: Unauthorized access receives HTTP 404 Not Found (for security)

## Access Control Matrix

| Action | User Status | Conversation Participation | Result |
|--------|-------------|---------------------------|---------|
| View Conversation | Authenticated | Participant | ✅ Allowed |
| View Conversation | Authenticated | Non-participant | ❌ 404 Forbidden |
| View Conversation | Unauthenticated | Any | ❌ 401 Unauthorized |
| Send Message | Authenticated | Participant | ✅ Allowed |
| Send Message | Authenticated | Non-participant | ❌ 404 Forbidden |
| Send Message | Unauthenticated | Any | ❌ 401 Unauthorized |
| Update Message | Authenticated | Participant | ✅ Allowed |
| Update Message | Authenticated | Non-participant | ❌ 404 Forbidden |
| Delete Message | Authenticated | Participant | ✅ Allowed |
| Delete Message | Authenticated | Non-participant | ❌ 404 Forbidden |

## Testing

### Manual Testing

Run the comprehensive test script:

```bash
cd /home/victor/Desktop/Airbnb/alx-backend-python/messaging_app
python test_permissions.py
```

### Test Scenarios

The test script covers:

1. **User Registration**: Create two test users
2. **Unauthenticated Access**: Verify 401 responses
3. **Conversation Creation**: User creates their own conversation
4. **Message Sending**: User sends message in their conversation
5. **Cross-User Access Denial**: User 2 cannot access User 1's conversation
6. **Cross-User Message Denial**: User 2 cannot send messages to User 1's conversation
7. **Cross-User View Denial**: User 2 cannot view User 1's messages
8. **Own Data Access**: User 1 can access their own conversation and messages
9. **Message Updates**: User 1 can update their own messages
10. **Cross-User Update Denial**: User 2 cannot update User 1's messages

### Expected Test Results

```
🔐 Testing IsParticipantOfConversation Permission Control
============================================================

1. Creating Test Users...
✅ User 1 (Alice) created successfully
✅ User 2 (Bob) created successfully

2. Testing Unauthenticated Access (Should be Denied)...
✅ Unauthenticated access correctly denied

3. User 1 Creating a Conversation...
✅ User 1 created conversation successfully

4. User 1 Sending a Message in Their Conversation...
✅ User 1 sent message successfully

5. User 2 Trying to Access User 1's Conversation (Should be Denied)...
✅ User 2 correctly denied access to User 1's conversation

6. User 2 Trying to Send Message to User 1's Conversation (Should be Denied)...
✅ User 2 correctly denied access to send message to User 1's conversation

7. User 2 Trying to View User 1's Message (Should be Denied)...
✅ User 2 correctly denied access to view User 1's message

8. User 1 Accessing Their Own Conversation and Messages...
✅ User 1 can access their own conversation
✅ User 1 can access their own message

9. User 1 Updating Their Own Message...
✅ User 1 successfully updated their message

10. User 2 Trying to Update User 1's Message (Should be Denied)...
✅ User 2 correctly denied access to update User 1's message

============================================================
🎉 All permission tests completed!
```

## Security Benefits

1. **Data Isolation**: Users can only access their own conversations and messages
2. **Authentication Enforcement**: All API endpoints require authentication
3. **Granular Control**: Permission checks at both view and object levels
4. **Global Application**: Default permission applies to all viewsets automatically
5. **Consistent Behavior**: Same permission logic across all conversation and message operations

## API Endpoints Affected

All conversation and message endpoints now use the custom permission:

- `GET /api/conversations/` - List user's conversations
- `POST /api/conversations/` - Create conversation
- `GET /api/conversations/{id}/` - Get specific conversation
- `PUT /api/conversations/{id}/` - Update conversation
- `DELETE /api/conversations/{id}/` - Delete conversation
- `GET /api/messages/` - List user's messages
- `POST /api/messages/` - Send message
- `GET /api/messages/{id}/` - Get specific message
- `PUT /api/messages/{id}/` - Update message
- `DELETE /api/messages/{id}/` - Delete message

## Error Responses

- **401 Unauthorized**: When user is not authenticated
- **404 Not Found**: When user tries to access conversations/messages they don't participate in
- **403 Forbidden**: When user lacks specific permissions (if any additional checks are added)

The 404 response for unauthorized access is intentional for security - it prevents information leakage about the existence of conversations or messages.
