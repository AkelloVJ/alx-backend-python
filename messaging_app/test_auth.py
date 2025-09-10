#!/usr/bin/env python3
"""
Test script to demonstrate JWT authentication functionality
Run this after installing dependencies and running migrations
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def test_authentication():
    """Test the complete authentication flow"""
    
    print("🔐 Testing JWT Authentication Flow")
    print("=" * 50)
    
    # Test 1: Register a new user
    print("\n1. Testing User Registration...")
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+1234567890",
        "role": "guest"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
        if response.status_code == 201:
            print("✅ User registration successful")
            user_data = response.json()
            access_token = user_data.get('access')
            refresh_token = user_data.get('refresh')
            print(f"   User ID: {user_data['user']['user_id']}")
            print(f"   Access Token: {access_token[:20]}...")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure Django is running on localhost:8000")
        return
    
    # Test 2: Login with the registered user
    print("\n2. Testing User Login...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if response.status_code == 200:
            print("✅ User login successful")
            login_data = response.json()
            access_token = login_data.get('access')
            refresh_token = login_data.get('refresh')
            print(f"   Access Token: {access_token[:20]}...")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 3: Access protected endpoint with JWT token
    print("\n3. Testing Protected Endpoint Access...")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
        if response.status_code == 200:
            print("✅ Profile access successful")
            profile = response.json()
            print(f"   User: {profile['first_name']} {profile['last_name']}")
            print(f"   Email: {profile['email']}")
        else:
            print(f"❌ Profile access failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 4: Create a conversation
    print("\n4. Testing Conversation Creation...")
    conversation_data = {
        "participants_id": profile['user_id']
    }
    
    try:
        response = requests.post(f"{BASE_URL}/conversations/", json=conversation_data, headers=headers)
        if response.status_code == 201:
            print("✅ Conversation creation successful")
            conversation = response.json()
            conversation_id = conversation['conversation_id']
            print(f"   Conversation ID: {conversation_id}")
        else:
            print(f"❌ Conversation creation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 5: Send a message
    print("\n5. Testing Message Creation...")
    message_data = {
        "conversation": conversation_id,
        "message_body": "Hello, this is a test message!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/messages/", json=message_data, headers=headers)
        if response.status_code == 201:
            print("✅ Message creation successful")
            message = response.json()
            print(f"   Message: {message['message_body']}")
        else:
            print(f"❌ Message creation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 6: Test token refresh
    print("\n6. Testing Token Refresh...")
    refresh_data = {
        "refresh": refresh_token
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token/refresh/", json=refresh_data)
        if response.status_code == 200:
            print("✅ Token refresh successful")
            new_tokens = response.json()
            new_access_token = new_tokens.get('access')
            print(f"   New Access Token: {new_access_token[:20]}...")
        else:
            print(f"❌ Token refresh failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 7: Test logout (token blacklisting)
    print("\n7. Testing Logout...")
    logout_data = {
        "refresh": refresh_token
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/logout/", json=logout_data, headers=headers)
        if response.status_code == 200:
            print("✅ Logout successful")
            print("   Refresh token has been blacklisted")
        else:
            print(f"❌ Logout failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    print("\n" + "=" * 50)
    print("🎉 All authentication tests completed!")
    print("\nAvailable API Endpoints:")
    print(f"  POST {BASE_URL}/auth/register/     - Register new user")
    print(f"  POST {BASE_URL}/auth/login/        - Login user")
    print(f"  POST {BASE_URL}/auth/token/        - Get JWT tokens")
    print(f"  POST {BASE_URL}/auth/token/refresh/ - Refresh JWT token")
    print(f"  POST {BASE_URL}/auth/logout/       - Logout user")
    print(f"  GET  {BASE_URL}/auth/profile/      - Get user profile")
    print(f"  PUT  {BASE_URL}/auth/profile/update/ - Update user profile")
    print(f"  GET  {BASE_URL}/conversations/     - List conversations")
    print(f"  POST {BASE_URL}/conversations/     - Create conversation")
    print(f"  GET  {BASE_URL}/messages/          - List messages")
    print(f"  POST {BASE_URL}/messages/          - Send message")

if __name__ == "__main__":
    test_authentication()
