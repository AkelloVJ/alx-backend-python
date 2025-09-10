# Django Middleware Project

This project demonstrates the implementation of custom Django middleware following best practices for modular architecture and separation of concerns.

## 🏗️ Project Structure

```
Django-Middleware-0x03/
├── config/                          # Main project configuration
│   ├── __init__.py
│   ├── settings.py                  # Django settings
│   ├── urls.py                      # Main URL configuration
│   └── wsgi.py                      # WSGI configuration
├── apps/                            # Applications directory
│   ├── __init__.py
│   ├── core/                        # Core functionality
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── middleware/              # Custom middleware
│   │       ├── __init__.py
│   │       ├── request_logging.py   # Request logging middleware
│   │       ├── time_restriction.py  # Time-based access control
│   │       ├── rate_limiting.py     # Rate limiting middleware
│   │       ├── role_permissions.py  # Role-based access control
│   │       ├── security_headers.py  # Security headers middleware
│   │       └── data_filtering.py    # Request data filtering
│   ├── users/                       # Users application
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── urls.py
│   │   └── views.py
│   └── listings/                    # Listings application
│       ├── __init__.py
│       ├── apps.py
│       ├── urls.py
│       └── views.py
├── manage.py                        # Django management script
├── test_middleware_structure.py     # Test script
└── README.md                        # This file
```

## 🎯 Learning Objectives

By completing this project, you will understand:

- **Middleware Lifecycle**: How Django middleware processes requests and responses
- **Custom Middleware**: Creating reusable middleware components
- **Security Patterns**: Implementing various security measures
- **Performance Optimization**: Efficient data structures and algorithms
- **Error Handling**: Proper HTTP status codes and error messages
- **Logging**: Comprehensive request and response logging
- **Testing**: Automated testing of middleware functionality
- **Modular Architecture**: Best practices for organizing Django projects

## 🔧 Implemented Middleware

### 1. Request Logging Middleware
**File**: `apps/core/middleware/request_logging.py`

Logs all incoming requests with timestamp, user information, and request path.

**Features**:
- Logs to `requests.log` file
- Includes user information (username/email or Anonymous)
- Records request path and timestamp
- Configurable logging levels

### 2. Time Restriction Middleware
**File**: `apps/core/middleware/time_restriction.py`

Restricts access to messaging endpoints during certain hours (6PM to 9PM only).

**Features**:
- Time-based access control
- Returns 403 Forbidden outside allowed hours
- Configurable time window
- Only affects messaging endpoints

### 3. Rate Limiting Middleware
**File**: `apps/core/middleware/rate_limiting.py`

Limits the number of messages a user can send within a time window (5 messages per minute).

**Features**:
- IP-based rate limiting
- Time window enforcement (1 minute)
- Configurable message limits
- Automatic cleanup of old requests

### 4. Role Permission Middleware
**File**: `apps/core/middleware/role_permissions.py`

Checks user roles before allowing access to specific actions (admin/moderator only).

**Features**:
- Role-based access control
- Protects admin endpoints
- Returns 403 for unauthorized roles
- Configurable allowed roles

### 5. Security Headers Middleware
**File**: `apps/core/middleware/security_headers.py`

Adds security headers to all responses.

**Features**:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin

### 6. Data Filtering Middleware
**File**: `apps/core/middleware/data_filtering.py`

Filters and cleans incoming request data before it reaches views.

**Features**:
- Data sanitization
- Request logging for debugging
- Input validation preparation

## ⚙️ Configuration

### Middleware Order
The middleware is configured in `config/settings.py` in the correct order:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'apps.core.middleware.request_logging.RequestLoggingMiddleware',
    'apps.core.middleware.security_headers.SecurityHeadersMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.core.middleware.role_permissions.RolePermissionMiddleware',
    'apps.core.middleware.time_restriction.RestrictAccessByTimeMiddleware',
    'apps.core.middleware.rate_limiting.OffensiveLanguageMiddleware',
    'apps.core.middleware.data_filtering.RequestDataFilteringMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### Logging Configuration
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'requests.log',
        },
    },
    'loggers': {
        'apps.core.middleware': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Start the Server
```bash
python manage.py runserver
```

### 4. Test the Middleware
```bash
python test_middleware_structure.py
```

## 🧪 Testing

### Manual Testing
1. **Request Logging**: Make any API request and check `requests.log`
2. **Time Restrictions**: Access `/api/messages/` outside 6PM-9PM
3. **Rate Limiting**: Send more than 5 POST requests to `/api/messages/`
4. **Role Permissions**: Try to access `/api/users/` without proper role
5. **Security Headers**: Check response headers for security headers

### Automated Testing
Run the test script to verify all middleware functionality:

```bash
python test_middleware_structure.py
```

## 📊 API Endpoints

### Core Endpoints
- `GET /api/test/` - Basic test endpoint
- `GET /api/messages/` - Messages endpoint (time restricted)
- `POST /api/messages/` - Create message (rate limited)
- `GET /api/conversations/` - Conversations endpoint

### Protected Endpoints (Role Required)
- `GET /api/users/` - User management (admin/moderator only)
- `GET /api/admin/` - Admin panel (admin/moderator only)

### Public Endpoints
- `GET /api/listings/` - Listings endpoint (public)

## 🔍 Key Features

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

## 🎯 Best Practices Implemented

1. **Single Responsibility**: Each middleware has one clear purpose
2. **Proper Ordering**: Middleware ordered correctly in settings
3. **Error Handling**: Graceful error responses
4. **Performance**: Efficient data structures for rate limiting
5. **Configurability**: Easy to modify parameters
6. **Logging**: Comprehensive request logging
7. **Security**: Multiple layers of protection
8. **Modular Architecture**: Clean separation of concerns
9. **Testing**: Automated testing capabilities
10. **Documentation**: Clear inline comments and documentation

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

## 🚨 Important Notes

1. **Time Restrictions**: Currently set to 6PM-9PM (18:00-21:00)
2. **Rate Limiting**: 5 messages per minute per IP address
3. **Role Permissions**: Only admin/moderator can access user management
4. **Logging**: All requests are logged to `requests.log`
5. **Security Headers**: Added to all responses automatically

## 🎉 Learning Outcomes

This project demonstrates:

- **Middleware Lifecycle**: Understanding request/response flow
- **Custom Middleware**: Creating reusable middleware components
- **Security Patterns**: Implementing various security measures
- **Performance Optimization**: Efficient data structures and algorithms
- **Error Handling**: Proper HTTP status codes and error messages
- **Logging**: Comprehensive request and response logging
- **Testing**: Automated testing of middleware functionality
- **Modular Architecture**: Best practices for organizing Django projects

The middleware implementation provides a robust foundation for building secure, scalable Django applications with proper access control, monitoring, and security features.
