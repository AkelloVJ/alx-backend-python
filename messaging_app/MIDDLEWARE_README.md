# Django Middleware Implementation

This project implements custom Django middleware components for the messaging app, demonstrating various middleware patterns and use cases.

## 🏗️ Project Structure

```
Django-Middleware-0x03/
├── chats/
│   ├── middleware.py          # All custom middleware classes
│   ├── models.py             # User, Conversation, Message models
│   ├── views.py              # API views
│   └── ...
├── messaging_app/
│   └── settings.py           # Middleware configuration
├── test_middleware.py        # Middleware testing script
├── requests.log              # Request logging file (generated)
└── MIDDLEWARE_README.md      # This documentation
```

## 🔧 Implemented Middleware Classes

### 1. RequestLoggingMiddleware
**Purpose**: Logs each user's requests to a file with timestamp, user, and request path.

**Features**:
- Logs all incoming requests
- Includes user information (username/email or Anonymous)
- Records request path and timestamp
- Writes to `requests.log` file

**Implementation**:
```python
def __call__(self, request):
    user = getattr(request, 'user', None)
    user_info = user.username if user and hasattr(user, 'username') else "Anonymous"
    log_message = f"{datetime.now()} - User: {user_info} - Path: {request.path}"
    logger.info(log_message)
    return self.get_response(request)
```

### 2. RestrictAccessByTimeMiddleware
**Purpose**: Restricts access to messaging app during certain hours (6PM to 9PM only).

**Features**:
- Time-based access control
- Returns 403 Forbidden outside allowed hours
- Configurable time window
- Only affects messaging endpoints

**Implementation**:
```python
def __call__(self, request):
    if request.path.startswith('/api/') and 'messages' in request.path:
        current_time = datetime.now().time()
        if not (dt_time(18, 0) <= current_time <= dt_time(21, 0)):
            return JsonResponse({'error': 'Access denied'}, status=403)
    return self.get_response(request)
```

### 3. OffensiveLanguageMiddleware (Rate Limiting)
**Purpose**: Limits the number of chat messages a user can send within a time window (5 messages per minute).

**Features**:
- IP-based rate limiting
- Time window enforcement (1 minute)
- Configurable message limits
- Automatic cleanup of old requests

**Implementation**:
```python
def __call__(self, request):
    if request.method == 'POST' and 'messages' in request.path:
        ip_address = self.get_client_ip(request)
        if len(self.request_counts[ip_address]) >= self.max_requests:
            return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
        self.request_counts[ip_address].append(time.time())
    return self.get_response(request)
```

### 4. RolePermissionMiddleware
**Purpose**: Checks user roles before allowing access to specific actions (admin/moderator only).

**Features**:
- Role-based access control
- Protects admin endpoints
- Returns 403 for unauthorized roles
- Configurable allowed roles

**Implementation**:
```python
def __call__(self, request):
    if any(request.path.startswith(endpoint) for endpoint in self.protected_endpoints):
        user = getattr(request, 'user', None)
        if not user or user.role not in self.allowed_roles:
            return JsonResponse({'error': 'Access denied'}, status=403)
    return self.get_response(request)
```

### 5. RequestDataFilteringMiddleware
**Purpose**: Filters and cleans incoming request data before it reaches views.

**Features**:
- Data sanitization
- Request logging for debugging
- Input validation preparation

### 6. SecurityHeadersMiddleware
**Purpose**: Adds security headers to all responses.

**Features**:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin

## ⚙️ Middleware Configuration

The middleware is configured in `settings.py` in the correct order:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'chats.middleware.RequestLoggingMiddleware',      # Log all requests
    'chats.middleware.SecurityHeadersMiddleware',     # Add security headers
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'chats.middleware.RolePermissionMiddleware',      # Check user roles
    'chats.middleware.RestrictAccessByTimeMiddleware', # Time restrictions
    'chats.middleware.OffensiveLanguageMiddleware',   # Rate limiting
    'chats.middleware.RequestDataFilteringMiddleware', # Data filtering
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

## 🧪 Testing the Middleware

### 1. Start the Server
```bash
cd Django-Middleware-0x03
python manage.py runserver
```

### 2. Run the Test Script
```bash
python test_middleware.py
```

### 3. Manual Testing

#### Test Request Logging
- Make any API request
- Check `requests.log` file for logged requests

#### Test Time Restrictions
- Access messaging endpoints outside 6PM-9PM
- Should receive 403 Forbidden response

#### Test Rate Limiting
- Send more than 5 messages within 1 minute
- Should receive 429 Too Many Requests after 5th message

#### Test Role Permissions
- Try to access `/api/users/` with regular user
- Should receive 403 Forbidden

#### Test Security Headers
- Make any API request
- Check response headers for security headers

## 📊 Middleware Order and Flow

1. **SecurityMiddleware** - Basic security features
2. **RequestLoggingMiddleware** - Log all requests
3. **SecurityHeadersMiddleware** - Add security headers to responses
4. **SessionMiddleware** - Handle sessions
5. **CommonMiddleware** - Common functionality
6. **CsrfViewMiddleware** - CSRF protection
7. **AuthenticationMiddleware** - User authentication
8. **RolePermissionMiddleware** - Role-based access control
9. **RestrictAccessByTimeMiddleware** - Time-based restrictions
10. **OffensiveLanguageMiddleware** - Rate limiting
11. **RequestDataFilteringMiddleware** - Data filtering
12. **MessageMiddleware** - Django messages
13. **XFrameOptionsMiddleware** - Clickjacking protection

## 🔍 Key Features Demonstrated

### Request Lifecycle
- **Request Interception**: Middleware processes requests before views
- **Response Modification**: Middleware can modify responses
- **Early Termination**: Middleware can return responses without reaching views

### Security Patterns
- **Authentication**: Verify user identity
- **Authorization**: Check user permissions
- **Rate Limiting**: Prevent abuse
- **Time Restrictions**: Control access hours
- **Input Filtering**: Sanitize data

### Logging and Monitoring
- **Request Logging**: Track all API usage
- **User Tracking**: Monitor user activities
- **Performance Monitoring**: Track request patterns

## 🚀 Best Practices Implemented

1. **Single Responsibility**: Each middleware has one clear purpose
2. **Proper Ordering**: Middleware ordered correctly in settings
3. **Error Handling**: Graceful error responses
4. **Performance**: Efficient data structures for rate limiting
5. **Configurability**: Easy to modify parameters
6. **Logging**: Comprehensive request logging
7. **Security**: Multiple layers of protection

## 📝 Log Files

### requests.log
Contains logged requests in the format:
```
2024-01-15 10:30:45,123 - INFO - 2024-01-15 10:30:45.123456 - User: test@example.com - Path: /api/messages/
```

## 🔧 Configuration Options

### Rate Limiting
- `max_requests`: Maximum messages per time window (default: 5)
- `time_window`: Time window in seconds (default: 60)

### Time Restrictions
- `start_time`: Allowed start time (default: 18:00)
- `end_time`: Allowed end time (default: 21:00)

### Role Permissions
- `allowed_roles`: List of allowed roles (default: ['admin', 'moderator'])
- `protected_endpoints`: List of protected URL patterns

## 🎯 Learning Outcomes

This implementation demonstrates:

1. **Middleware Lifecycle**: Understanding request/response flow
2. **Custom Middleware**: Creating reusable middleware components
3. **Security Patterns**: Implementing various security measures
4. **Performance Optimization**: Efficient data structures and algorithms
5. **Error Handling**: Proper HTTP status codes and error messages
6. **Logging**: Comprehensive request and response logging
7. **Testing**: Automated testing of middleware functionality

## 🚨 Important Notes

1. **Time Restrictions**: Currently set to 6PM-9PM (18:00-21:00)
2. **Rate Limiting**: 5 messages per minute per IP address
3. **Role Permissions**: Only admin/moderator can access user management
4. **Logging**: All requests are logged to `requests.log`
5. **Security Headers**: Added to all responses automatically

The middleware implementation provides a robust foundation for building secure, scalable Django applications with proper access control, monitoring, and security features.
