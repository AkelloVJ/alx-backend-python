# Postman Collections for Messaging App API

This directory contains Postman collections for testing the Django Messaging App API with JWT authentication, pagination, and filtering.

## Files Included

### 1. Messaging_App_API.postman_collection.json
**Complete API Collection** - Comprehensive collection with all endpoints organized by functionality:
- **Authentication**: User registration, login, token refresh, logout, profile management
- **Conversations**: CRUD operations, filtering, search
- **Messages**: CRUD operations, filtering, search, pagination
- **Users**: User management (admin functions)
- **Security Tests**: Unauthorized access, cross-user security tests

### 2. API_Requirements_Test.postman_collection.json
**Requirements Verification Collection** - Specific tests to verify all API requirements:
- ✅ PUT, PATCH, DELETE method support
- ✅ BasicAuthentication support
- ✅ PageNumberPagination implementation
- ✅ MessageFilter functionality
- ✅ Permission enforcement
- ✅ Security tests

### 3. Messaging_App_Environment.postman_environment.json
**Environment Variables** - Pre-configured environment with:
- Base URL: `http://127.0.0.1:8000`
- Auto-extraction of tokens and IDs from responses
- Secure storage of sensitive data

## How to Use

### 1. Import Collections
1. Open Postman
2. Click "Import" button
3. Select all three JSON files from this directory
4. Import the environment file as well

### 2. Set Up Environment
1. Select "Messaging App Environment" from the environment dropdown
2. The base URL is pre-configured to `http://127.0.0.1:8000`
3. Tokens and IDs will be automatically extracted from responses

### 3. Run Tests

#### Quick Start (Requirements Test)
1. Select "API Requirements Test" collection
2. Click "Run" button
3. All tests will run in sequence and verify requirements

#### Manual Testing
1. Start with "Authentication" folder
2. Run "Register User" first
3. Run "Login User" to get tokens
4. Use other endpoints as needed

### 4. Automated Testing
The collections include automated tests that:
- Verify response status codes
- Check response structure
- Auto-extract tokens and IDs
- Validate pagination and filtering
- Test security features

## Test Coverage

### Authentication Tests
- ✅ User registration with validation
- ✅ JWT login and token generation
- ✅ Token refresh functionality
- ✅ Secure logout with token blacklisting
- ✅ Profile management

### CRUD Operations Tests
- ✅ **PUT Method**: Full resource updates
- ✅ **PATCH Method**: Partial resource updates  
- ✅ **DELETE Method**: Resource deletion
- ✅ **GET Method**: Resource retrieval
- ✅ **POST Method**: Resource creation

### Pagination Tests
- ✅ PageNumberPagination implementation
- ✅ Custom page sizes
- ✅ Page navigation
- ✅ Pagination metadata

### Filtering Tests
- ✅ MessageFilter by content (`message_contains`)
- ✅ MessageFilter by sender (`sender`)
- ✅ MessageFilter by date range (`sent_after`, `sent_before`)
- ✅ Search functionality
- ✅ Ordering options

### Security Tests
- ✅ Unauthorized access protection (401)
- ✅ Cross-user access denial (404)
- ✅ JWT token validation
- ✅ Permission enforcement
- ✅ BasicAuthentication support

## Environment Variables

The collections use these environment variables:

| Variable | Description | Auto-Extracted |
|----------|-------------|----------------|
| `base_url` | API base URL | No |
| `access_token` | JWT access token | Yes |
| `refresh_token` | JWT refresh token | Yes |
| `user_id` | Current user ID | Yes |
| `conversation_id` | Current conversation ID | Yes |
| `message_id` | Current message ID | Yes |
| `other_user_token` | Token for cross-user tests | Manual |

## API Endpoints Tested

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/` - Get JWT tokens
- `POST /api/auth/token/refresh/` - Refresh tokens
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update profile

### Conversation Endpoints
- `GET /api/conversations/` - List conversations
- `POST /api/conversations/` - Create conversation
- `GET /api/conversations/{id}/` - Get conversation
- `PUT /api/conversations/{id}/` - Update conversation
- `PATCH /api/conversations/{id}/` - Partial update
- `DELETE /api/conversations/{id}/` - Delete conversation

### Message Endpoints
- `GET /api/messages/` - List messages
- `POST /api/messages/` - Send message
- `GET /api/messages/{id}/` - Get message
- `PUT /api/messages/{id}/` - Update message
- `PATCH /api/messages/{id}/` - Partial update
- `DELETE /api/messages/{id}/` - Delete message

### User Endpoints
- `GET /api/users/` - List users
- `GET /api/users/{id}/` - Get user
- `PUT /api/users/{id}/` - Update user
- `PATCH /api/users/{id}/` - Partial update
- `DELETE /api/users/{id}/` - Delete user

## Prerequisites

1. **Django Server Running**: Ensure the Django development server is running on `http://127.0.0.1:8000`
2. **Database Migrated**: Run migrations to set up the database
3. **Dependencies Installed**: All required packages should be installed

## Running the Server

```bash
cd /home/victor/Desktop/Airbnb/alx-backend-python/messaging_app
source ../venv/bin/activate
python manage.py runserver
```

## Test Results

When you run the collections, you should see:
- ✅ All authentication tests passing
- ✅ All CRUD operations working (PUT, PATCH, DELETE)
- ✅ Pagination working correctly
- ✅ Filtering and search functioning
- ✅ Security tests confirming proper access control
- ✅ BasicAuthentication support verified

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Make sure to run authentication tests first
2. **404 Not Found**: Check if the server is running and accessible
3. **Token Issues**: Ensure login/registration was successful
4. **Environment Variables**: Verify the environment is selected

### Debug Tips

1. Check the Postman console for detailed error messages
2. Verify the server is running on the correct port
3. Ensure all required environment variables are set
4. Check the Django server logs for any errors

## Requirements Verification

This collection specifically tests the following requirements:

- ✅ **PUT, PATCH, DELETE Methods**: All CRUD operations supported
- ✅ **BasicAuthentication**: Added to settings.py and tested
- ✅ **PageNumberPagination**: Implemented and verified
- ✅ **MessageFilter**: Filtering by content, sender, date range
- ✅ **Permission Control**: Only participants can access conversations
- ✅ **Security**: Unauthorized access properly denied

The collections provide comprehensive testing coverage for all API functionality and requirements.
