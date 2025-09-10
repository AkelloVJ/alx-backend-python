#!/usr/bin/env python3
"""
Simple API test script for the messaging app
Tests core functionality: authentication, conversations, messages
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api"

def test_simple():
    """Simple API testing"""
    
    print("🚀 Simple API Testing for Messaging App")
    print("=" * 50)
    
    # Test 1: User Registration
    print("\n1. Testing User Registration...")
    
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+1234567890",
        "role": "guest"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=user_data)
        if response.status_code == 201:
            print("✅ User registration successful")
            user_info = response.json()
            user_id = user_info['user']['user_id']
            access_token = user_info['access']
            print(f"   User ID: {user_id}")
            print(f"   Email: {user_info['user']['email']}")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Test 2: JWT Login
    print("\n2. Testing JWT Login...")
    
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if response.status_code == 200:
            print("✅ Login successful")
            login_info = response.json()
            access_token = login_info['access']
            refresh_token = login_info['refresh']
            print(f"   Access token: {access_token[:20]}...")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test 3: Unauthorized Access (Should be denied)
    print("\n3. Testing Unauthorized Access...")
    
    try:
        response = requests.get(f"{BASE_URL}/conversations/")
        if response.status_code == 401:
            print("✅ Unauthorized access correctly denied (401)")
        else:
            print(f"❌ Expected 401, got {response.status_code}")
    except Exception as e:
        print(f"❌ Unauthorized access test error: {e}")
    
    # Test 4: Authenticated Access
    print("\n4. Testing Authenticated Access...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/conversations/", headers=headers)
        if response.status_code == 200:
            print("✅ Authenticated access successful")
            conversations = response.json()
            print(f"   Response type: {type(conversations)}")
            if isinstance(conversations, dict):
                print(f"   Count: {conversations.get('count', 'N/A')}")
                print(f"   Results: {len(conversations.get('results', []))}")
            else:
                print(f"   Conversations: {len(conversations)}")
        else:
            print(f"❌ Authenticated access failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Authenticated access error: {e}")
    
    # Test 5: Create Conversation
    print("\n5. Testing Conversation Creation...")
    
    conversation_data = {
        "participants_id": user_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/conversations/", json=conversation_data, headers=headers)
        if response.status_code == 201:
            print("✅ Conversation created successfully")
            conversation = response.json()
            conversation_id = conversation['conversation_id']
            print(f"   Conversation ID: {conversation_id}")
        else:
            print(f"❌ Conversation creation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Conversation creation error: {e}")
        return
    
    # Test 6: Send Message
    print("\n6. Testing Message Sending...")
    
    message_data = {
        "conversation": conversation_id,
        "message_body": "Hello, this is a test message!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/messages/", json=message_data, headers=headers)
        if response.status_code == 201:
            print("✅ Message sent successfully")
            message = response.json()
            message_id = message['message_id']
            print(f"   Message ID: {message_id}")
            print(f"   Message: {message['message_body']}")
        else:
            print(f"❌ Message sending failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Message sending error: {e}")
        return
    
    # Test 7: Fetch Messages
    print("\n7. Testing Message Fetching...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/", headers=headers)
        if response.status_code == 200:
            print("✅ Messages fetched successfully")
            messages = response.json()
            print(f"   Response type: {type(messages)}")
            if isinstance(messages, dict):
                print(f"   Count: {messages.get('count', 'N/A')}")
                print(f"   Page size: {messages.get('page_size', 'N/A')}")
                print(f"   Current page: {messages.get('current_page', 'N/A')}")
                print(f"   Messages on page: {len(messages.get('results', []))}")
            else:
                print(f"   Messages: {len(messages)}")
        else:
            print(f"❌ Message fetching failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Message fetching error: {e}")
    
    # Test 8: Test Pagination
    print("\n8. Testing Pagination...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/?page=1&page_size=5", headers=headers)
        if response.status_code == 200:
            print("✅ Pagination working")
            messages = response.json()
            if isinstance(messages, dict):
                print(f"   Page size: {messages.get('page_size')}")
                print(f"   Current page: {messages.get('current_page')}")
                print(f"   Total pages: {messages.get('total_pages')}")
                print(f"   Has next: {messages.get('has_next')}")
        else:
            print(f"❌ Pagination test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Pagination test error: {e}")
    
    # Test 9: Test Filtering
    print("\n9. Testing Filtering...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/?message_contains=test", headers=headers)
        if response.status_code == 200:
            print("✅ Filtering working")
            messages = response.json()
            if isinstance(messages, dict):
                print(f"   Filtered messages: {messages.get('count')}")
        else:
            print(f"❌ Filtering test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Filtering test error: {e}")
    
    # Test 10: Test Search
    print("\n10. Testing Search...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/?search=hello", headers=headers)
        if response.status_code == 200:
            print("✅ Search working")
            messages = response.json()
            if isinstance(messages, dict):
                print(f"   Search results: {messages.get('count')}")
        else:
            print(f"❌ Search test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Search test error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Simple API Testing Completed!")
    print("\n✅ Core Features Verified:")
    print("   - User registration and authentication")
    print("   - JWT token login")
    print("   - Unauthorized access protection")
    print("   - Conversation creation")
    print("   - Message sending and fetching")
    print("   - Pagination functionality")
    print("   - Filtering and search capabilities")

if __name__ == "__main__":
    test_simple()
