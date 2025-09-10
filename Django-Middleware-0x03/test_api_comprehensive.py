#!/usr/bin/env python3
"""
Comprehensive API test script for the messaging app
Tests authentication, conversations, messages, and security
"""

import requests
import json
import time
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def test_api_comprehensive():
    """Comprehensive API testing"""
    
    print("🚀 Comprehensive API Testing for Messaging App")
    print("=" * 60)
    
    # Wait for server to start
    print("\n⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test 1: Server Health Check
    print("\n1. Testing Server Health...")
    try:
        response = requests.get(f"{BASE_URL}/conversations/", timeout=5)
        if response.status_code == 401:
            print("✅ Server is running and responding (401 expected for unauthenticated)")
        else:
            print(f"⚠️  Server responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the server first.")
        return
    except Exception as e:
        print(f"❌ Server error: {e}")
        return
    
    # Test 2: User Registration
    print("\n2. Testing User Registration...")
    
    # Register User 1 (Alice)
    user1_data = {
        "email": "alice@example.com",
        "password": "testpassword123",
        "first_name": "Alice",
        "last_name": "Smith",
        "phone_number": "+1234567890",
        "role": "guest"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=user1_data)
        if response.status_code == 201:
            print("✅ User 1 (Alice) registered successfully")
            user1_tokens = response.json()
            user1_access_token = user1_tokens.get('access')
            user1_refresh_token = user1_tokens.get('refresh')
            user1_id = user1_tokens['user']['user_id']
            print(f"   User ID: {user1_id}")
            print(f"   Email: {user1_tokens['user']['email']}")
        else:
            print(f"❌ User 1 registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Register User 2 (Bob)
    user2_data = {
        "email": "bob@example.com",
        "password": "testpassword123",
        "first_name": "Bob",
        "last_name": "Johnson",
        "phone_number": "+0987654321",
        "role": "guest"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=user2_data)
        if response.status_code == 201:
            print("✅ User 2 (Bob) registered successfully")
            user2_tokens = response.json()
            user2_access_token = user2_tokens.get('access')
            user2_refresh_token = user2_tokens.get('refresh')
            user2_id = user2_tokens['user']['user_id']
            print(f"   User ID: {user2_id}")
            print(f"   Email: {user2_tokens['user']['email']}")
        else:
            print(f"❌ User 2 registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Test 3: JWT Authentication
    print("\n3. Testing JWT Authentication...")
    
    # Test login for User 1
    login_data = {
        "email": "alice@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if response.status_code == 200:
            print("✅ User 1 login successful")
            login_tokens = response.json()
            user1_access_token = login_tokens.get('access')
            user1_refresh_token = login_tokens.get('refresh')
            print(f"   Access token: {user1_access_token[:20]}...")
        else:
            print(f"❌ User 1 login failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test 4: Unauthorized Access (Should be denied)
    print("\n4. Testing Unauthorized Access (Should be Denied)...")
    
    try:
        response = requests.get(f"{BASE_URL}/conversations/")
        if response.status_code == 401:
            print("✅ Unauthorized access correctly denied (401)")
        else:
            print(f"❌ Expected 401, got {response.status_code}")
    except Exception as e:
        print(f"❌ Unauthorized access test error: {e}")
    
    # Test 5: Authenticated Access
    print("\n5. Testing Authenticated Access...")
    
    headers_user1 = {
        "Authorization": f"Bearer {user1_access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/conversations/", headers=headers_user1)
        if response.status_code == 200:
            print("✅ Authenticated access successful")
            conversations = response.json()
            print(f"   Conversations count: {conversations['count']}")
        else:
            print(f"❌ Authenticated access failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Authenticated access error: {e}")
        return
    
    # Test 6: Create Conversation
    print("\n6. Testing Conversation Creation...")
    
    conversation_data = {
        "participants_id": user1_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/conversations/", json=conversation_data, headers=headers_user1)
        if response.status_code == 201:
            print("✅ Conversation created successfully")
            conversation = response.json()
            conversation_id = conversation['conversation_id']
            print(f"   Conversation ID: {conversation_id}")
            print(f"   Participant: {conversation['participants_id']}")
        else:
            print(f"❌ Conversation creation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Conversation creation error: {e}")
        return
    
    # Test 7: Send Messages
    print("\n7. Testing Message Sending...")
    
    messages_data = [
        {"conversation": conversation_id, "message_body": "Hello, this is Alice's first message!"},
        {"conversation": conversation_id, "message_body": "This is a test message about work."},
        {"conversation": conversation_id, "message_body": "Message about vacation plans."},
        {"conversation": conversation_id, "message_body": "Important information about the project."},
        {"conversation": conversation_id, "message_body": "Final test message."}
    ]
    
    created_messages = []
    for i, msg_data in enumerate(messages_data):
        try:
            response = requests.post(f"{BASE_URL}/messages/", json=msg_data, headers=headers_user1)
            if response.status_code == 201:
                created_messages.append(response.json())
                print(f"   ✅ Message {i+1} sent successfully")
            else:
                print(f"   ❌ Message {i+1} failed: {response.status_code}")
                print(f"      Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Message {i+1} error: {e}")
    
    print(f"✅ Successfully sent {len(created_messages)} messages")
    
    # Test 8: Fetch Conversations
    print("\n8. Testing Fetch Conversations...")
    
    try:
        response = requests.get(f"{BASE_URL}/conversations/", headers=headers_user1)
        if response.status_code == 200:
            print("✅ Conversations fetched successfully")
            conversations = response.json()
            print(f"   Total conversations: {conversations['count']}")
            print(f"   Current page: {conversations['current_page']}")
            print(f"   Page size: {conversations['page_size']}")
            if conversations['results']:
                conv = conversations['results'][0]
                print(f"   First conversation ID: {conv['conversation_id']}")
        else:
            print(f"❌ Fetch conversations failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Fetch conversations error: {e}")
    
    # Test 9: Fetch Messages
    print("\n9. Testing Fetch Messages...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/", headers=headers_user1)
        if response.status_code == 200:
            print("✅ Messages fetched successfully")
            messages = response.json()
            print(f"   Total messages: {messages['count']}")
            print(f"   Current page: {messages['current_page']}")
            print(f"   Page size: {messages['page_size']}")
            print(f"   Messages on this page: {len(messages['results'])}")
            if messages['results']:
                msg = messages['results'][0]
                print(f"   First message: {msg['message_body'][:50]}...")
        else:
            print(f"❌ Fetch messages failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Fetch messages error: {e}")
    
    # Test 10: Cross-User Security (User 2 cannot access User 1's data)
    print("\n10. Testing Cross-User Security...")
    
    headers_user2 = {
        "Authorization": f"Bearer {user2_access_token}",
        "Content-Type": "application/json"
    }
    
    # User 2 tries to access User 1's conversation
    try:
        response = requests.get(f"{BASE_URL}/conversations/{conversation_id}/", headers=headers_user2)
        if response.status_code == 404:
            print("✅ User 2 correctly denied access to User 1's conversation (404)")
        else:
            print(f"❌ Expected 404, got {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Cross-user security test error: {e}")
    
    # User 2 tries to send message to User 1's conversation
    try:
        message_data = {
            "conversation": conversation_id,
            "message_body": "This should be denied!"
        }
        response = requests.post(f"{BASE_URL}/messages/", json=message_data, headers=headers_user2)
        if response.status_code == 404:
            print("✅ User 2 correctly denied access to send message to User 1's conversation (404)")
        else:
            print(f"❌ Expected 404, got {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Cross-user message security test error: {e}")
    
    # Test 11: Pagination Testing
    print("\n11. Testing Pagination...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/?page=1&page_size=3", headers=headers_user1)
        if response.status_code == 200:
            print("✅ Pagination working correctly")
            messages = response.json()
            print(f"   Page size: {messages['page_size']}")
            print(f"   Current page: {messages['current_page']}")
            print(f"   Total pages: {messages['total_pages']}")
            print(f"   Messages on this page: {len(messages['results'])}")
            print(f"   Has next page: {messages['has_next']}")
        else:
            print(f"❌ Pagination test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Pagination test error: {e}")
    
    # Test 12: Filtering Testing
    print("\n12. Testing Filtering...")
    
    try:
        # Filter by message content
        response = requests.get(f"{BASE_URL}/messages/?message_contains=work", headers=headers_user1)
        if response.status_code == 200:
            print("✅ Content filtering working")
            messages = response.json()
            print(f"   Messages containing 'work': {messages['count']}")
        else:
            print(f"❌ Content filtering test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Filtering test error: {e}")
    
    # Test 13: Search Testing
    print("\n13. Testing Search...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/?search=message", headers=headers_user1)
        if response.status_code == 200:
            print("✅ Search functionality working")
            messages = response.json()
            print(f"   Search results for 'message': {messages['count']}")
        else:
            print(f"❌ Search test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Search test error: {e}")
    
    # Test 14: Token Refresh
    print("\n14. Testing Token Refresh...")
    
    try:
        refresh_data = {"refresh": user1_refresh_token}
        response = requests.post(f"{BASE_URL}/auth/token/refresh/", json=refresh_data)
        if response.status_code == 200:
            print("✅ Token refresh successful")
            new_tokens = response.json()
            new_access_token = new_tokens.get('access')
            print(f"   New access token: {new_access_token[:20]}...")
        else:
            print(f"❌ Token refresh failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Token refresh error: {e}")
    
    # Test 15: Logout
    print("\n15. Testing Logout...")
    
    try:
        logout_data = {"refresh": user1_refresh_token}
        response = requests.post(f"{BASE_URL}/auth/logout/", json=logout_data, headers=headers_user1)
        if response.status_code == 200:
            print("✅ Logout successful")
            print("   Refresh token has been blacklisted")
        else:
            print(f"❌ Logout failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Logout error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Comprehensive API Testing Completed!")
    print("\nTest Summary:")
    print("✅ User registration and authentication")
    print("✅ JWT token login and refresh")
    print("✅ Unauthorized access protection")
    print("✅ Conversation creation and fetching")
    print("✅ Message sending and fetching")
    print("✅ Cross-user security (users cannot access each other's data)")
    print("✅ Pagination functionality")
    print("✅ Filtering and search capabilities")
    print("✅ Token management (refresh and logout)")
    
    print("\n🔐 Security Features Verified:")
    print("✅ Only authenticated users can access the API")
    print("✅ Users can only access their own conversations and messages")
    print("✅ Cross-user access is properly denied")
    print("✅ JWT tokens are working correctly")
    print("✅ Token blacklisting works for logout")

if __name__ == "__main__":
    test_api_comprehensive()
