# JWT Authentication Implementation

This document describes the JWT (JSON Web Token) authentication implementation for the Django messaging app.

## Features Implemented

### 1. JWT Authentication Setup
- ✅ Installed `djangorestframework-simplejwt`
- ✅ Configured JWT settings in `settings.py`
- ✅ Added JWT authentication to REST framework configuration
- ✅ Configured token blacklisting for secure logout

### 2. Authentication Endpoints
- ✅ `POST /api/auth/register/` - Register new user
- ✅ `POST /api/auth/login/` - Login user
- ✅ `POST /api/auth/token/` - Get JWT tokens (alternative to login)
- ✅ `POST /api/auth/token/refresh/` - Refresh JWT token
- ✅ `POST /api/auth/logout/` - Logout user (blacklist token)
- ✅ `GET /api/auth/profile/` - Get user profile
- ✅ `PUT /api/auth/profile/update/` - Update user profile

### 3. Custom Permissions
- ✅ `IsConversationParticipant` - Only conversation participants can access conversations
- ✅ `IsMessageSenderOrConversationParticipant` - Message access control
- ✅ `IsOwnerOrAdmin` - User data access control
- ✅ `CanAccessOwnData` - Ensure users can only access their own data

### 4. Security Features
- ✅ JWT tokens with configurable expiration times
- ✅ Token rotation on refresh
- ✅ Token blacklisting for secure logout
- ✅ Password validation
- ✅ User-specific data access control

## Installation and Setup

### 1. Install Dependencies
```bash
cd /home/victor/Desktop/Airbnb/alx-backend-python
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
cd messaging_app
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 4. Start Development Server
```bash
python manage.py runserver
```

## API Usage Examples

### Register a New User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "role": "guest"
  }'
```

### Login User
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Access Protected Endpoints
```bash
# Get user profile
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Create a conversation
curl -X POST http://localhost:8000/api/conversations/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "participants_id": "USER_UUID"
  }'

# Send a message
curl -X POST http://localhost:8000/api/messages/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation": "CONVERSATION_UUID",
    "message_body": "Hello, this is a test message!"
  }'
```

### Refresh Token
```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'
```

### Logout
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'
```

## Testing

Run the test script to verify authentication functionality:

```bash
cd /home/victor/Desktop/Airbnb/alx-backend-python/messaging_app
python test_auth.py
```

## Security Considerations

1. **Token Expiration**: Access tokens expire in 60 minutes by default
2. **Refresh Tokens**: Valid for 7 days with rotation enabled
3. **Token Blacklisting**: Logout blacklists refresh tokens
4. **Password Validation**: Django's built-in password validators are used
5. **User Isolation**: Users can only access their own conversations and messages
6. **Admin Access**: Admins can access all data

## Configuration

JWT settings can be modified in `messaging_app/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    # ... other settings
}
```

## File Structure

```
messaging_app/
├── chats/
│   ├── auth.py              # Authentication views
│   ├── permissions.py       # Custom permissions
│   ├── views.py            # Updated with new permissions
│   ├── urls.py             # Updated with auth endpoints
│   └── models.py           # User, Conversation, Message models
├── messaging_app/
│   └── settings.py         # JWT configuration
└── test_auth.py           # Test script
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid credentials)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error

All error responses include descriptive error messages to help with debugging.
