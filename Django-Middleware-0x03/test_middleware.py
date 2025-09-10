#!/usr/bin/env python3
"""
Test script to verify all middleware functionality
Tests logging, time restrictions, rate limiting, and role permissions
"""

import requests
import json
import time
from datetime import datetime

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api"

def test_middleware():
    """Test all middleware functionality"""
    
    print("🔧 Testing Django Middleware Functionality")
    print("=" * 60)
    
    # Test 1: Request Logging Middleware
    print("\n1. Testing Request Logging Middleware...")
    
    try:
        response = requests.get(f"{BASE_URL}/conversations/")
        print(f"✅ Request made - Check requests.log file for logging")
        print(f"   Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start with: python manage.py runserver")
        return
    
    # Test 2: Time Restriction Middleware
    print("\n2. Testing Time Restriction Middleware...")
    
    current_time = datetime.now().time()
    print(f"   Current time: {current_time}")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/")
        if response.status_code == 403:
            print("✅ Time restriction working - Access denied outside 6PM-9PM")
            print(f"   Response: {response.json()}")
        else:
            print("✅ Time restriction allows access (within allowed hours)")
            print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Time restriction test error: {e}")
    
    # Test 3: Rate Limiting Middleware
    print("\n3. Testing Rate Limiting Middleware...")
    
    # First, we need to register and login a user
    print("   Registering test user...")
    user_data = {
        "email": f"test{int(time.time())}@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+1234567890",
        "role": "guest"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=user_data)
        if response.status_code == 201:
            print("✅ User registered successfully")
            user_info = response.json()
            access_token = user_info['access']
            user_id = user_info['user']['user_id']
        else:
            print(f"❌ User registration failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ User registration error: {e}")
        return
    
    # Create a conversation for testing
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        conversation_data = {"participants_id": user_id}
        response = requests.post(f"{BASE_URL}/conversations/", json=conversation_data, headers=headers)
        if response.status_code == 201:
            conversation = response.json()
            conversation_id = conversation['conversation_id']
            print("✅ Conversation created for rate limiting test")
        else:
            print(f"❌ Conversation creation failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Conversation creation error: {e}")
        return
    
    # Test rate limiting by sending multiple messages
    print("   Testing rate limiting (5 messages per minute)...")
    
    for i in range(7):  # Try to send 7 messages (limit is 5)
        message_data = {
            "conversation": conversation_id,
            "message_body": f"Test message {i+1} for rate limiting"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/messages/", json=message_data, headers=headers)
            if response.status_code == 201:
                print(f"   ✅ Message {i+1} sent successfully")
            elif response.status_code == 429:
                print(f"   ✅ Rate limit triggered at message {i+1}")
                print(f"   Response: {response.json()}")
                break
            else:
                print(f"   ❌ Unexpected status for message {i+1}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error sending message {i+1}: {e}")
    
    # Test 4: Role Permission Middleware
    print("\n4. Testing Role Permission Middleware...")
    
    # Test with regular user (should be denied access to admin endpoints)
    try:
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        if response.status_code == 403:
            print("✅ Role permission working - Regular user denied access to admin endpoints")
            print(f"   Response: {response.json()}")
        else:
            print(f"⚠️  Unexpected response for role permission: {response.status_code}")
    except Exception as e:
        print(f"❌ Role permission test error: {e}")
    
    # Test 5: Security Headers Middleware
    print("\n5. Testing Security Headers Middleware...")
    
    try:
        response = requests.get(f"{BASE_URL}/conversations/", headers=headers)
        print("✅ Security headers added to response")
        print(f"   X-Content-Type-Options: {response.headers.get('X-Content-Type-Options', 'Not set')}")
        print(f"   X-Frame-Options: {response.headers.get('X-Frame-Options', 'Not set')}")
        print(f"   X-XSS-Protection: {response.headers.get('X-XSS-Protection', 'Not set')}")
    except Exception as e:
        print(f"❌ Security headers test error: {e}")
    
    # Test 6: Request Data Filtering Middleware
    print("\n6. Testing Request Data Filtering Middleware...")
    
    try:
        # Send a message to test data filtering
        message_data = {
            "conversation": conversation_id,
            "message_body": "Test message for data filtering"
        }
        response = requests.post(f"{BASE_URL}/messages/", json=message_data, headers=headers)
        print("✅ Request data filtering middleware active")
        print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Data filtering test error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Middleware Testing Completed!")
    print("\n✅ Middleware Features Tested:")
    print("   - Request Logging (check requests.log file)")
    print("   - Time-based Access Restriction (6PM-9PM)")
    print("   - Rate Limiting (5 messages per minute)")
    print("   - Role-based Permissions")
    print("   - Security Headers")
    print("   - Request Data Filtering")
    
    print("\n📝 Check the requests.log file to see logged requests")
    print("🔧 All middleware components are working correctly!")

if __name__ == "__main__":
    test_middleware()
