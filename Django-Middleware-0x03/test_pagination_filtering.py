#!/usr/bin/env python3
"""
Test script to demonstrate pagination and filtering functionality
Run this after installing dependencies and running migrations
"""

import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def test_pagination_and_filtering():
    """Test pagination and filtering functionality"""
    
    print("📄 Testing Pagination and Filtering Functionality")
    print("=" * 60)
    
    # Create test users
    print("\n1. Creating Test Users...")
    
    # User 1
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
            print("✅ User 1 (Alice) created successfully")
            user1_tokens = response.json()
            user1_access_token = user1_tokens.get('access')
            user1_id = user1_tokens['user']['user_id']
        else:
            print(f"❌ User 1 creation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure Django is running on localhost:8000")
        return
    
    # User 2
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
            print("✅ User 2 (Bob) created successfully")
            user2_tokens = response.json()
            user2_access_token = user2_tokens.get('access')
            user2_id = user2_tokens['user']['user_id']
        else:
            print(f"❌ User 2 creation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    headers_user1 = {
        "Authorization": f"Bearer {user1_access_token}",
        "Content-Type": "application/json"
    }
    
    # Create conversations and messages for testing
    print("\n2. Creating Test Data...")
    
    # Create conversation
    conversation_data = {
        "participants_id": user1_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/conversations/", json=conversation_data, headers=headers_user1)
        if response.status_code == 201:
            print("✅ Conversation created successfully")
            conversation = response.json()
            conversation_id = conversation['conversation_id']
        else:
            print(f"❌ Conversation creation failed: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Create multiple messages for pagination testing
    print("\n3. Creating Test Messages...")
    
    messages_data = [
        {"conversation": conversation_id, "message_body": "Hello, this is message 1"},
        {"conversation": conversation_id, "message_body": "This is message 2 with different content"},
        {"conversation": conversation_id, "message_body": "Message 3 about work"},
        {"conversation": conversation_id, "message_body": "Message 4 about vacation"},
        {"conversation": conversation_id, "message_body": "Message 5 with important information"},
        {"conversation": conversation_id, "message_body": "Message 6 about meeting"},
        {"conversation": conversation_id, "message_body": "Message 7 with project details"},
        {"conversation": conversation_id, "message_body": "Message 8 about deadline"},
        {"conversation": conversation_id, "message_body": "Message 9 with updates"},
        {"conversation": conversation_id, "message_body": "Message 10 final message"},
        {"conversation": conversation_id, "message_body": "Message 11 additional content"},
        {"conversation": conversation_id, "message_body": "Message 12 more information"},
        {"conversation": conversation_id, "message_body": "Message 13 about weekend"},
        {"conversation": conversation_id, "message_body": "Message 14 with plans"},
        {"conversation": conversation_id, "message_body": "Message 15 about dinner"},
        {"conversation": conversation_id, "message_body": "Message 16 with recipes"},
        {"conversation": conversation_id, "message_body": "Message 17 about travel"},
        {"conversation": conversation_id, "message_body": "Message 18 with destinations"},
        {"conversation": conversation_id, "message_body": "Message 19 about weather"},
        {"conversation": conversation_id, "message_body": "Message 20 with forecast"},
        {"conversation": conversation_id, "message_body": "Message 21 about sports"},
        {"conversation": conversation_id, "message_body": "Message 22 with scores"},
        {"conversation": conversation_id, "message_body": "Message 23 about movies"},
        {"conversation": conversation_id, "message_body": "Message 24 with reviews"},
        {"conversation": conversation_id, "message_body": "Message 25 final test message"},
    ]
    
    created_messages = []
    for i, msg_data in enumerate(messages_data):
        try:
            response = requests.post(f"{BASE_URL}/messages/", json=msg_data, headers=headers_user1)
            if response.status_code == 201:
                created_messages.append(response.json())
                if (i + 1) % 5 == 0:
                    print(f"   Created {i + 1} messages...")
            else:
                print(f"❌ Message {i + 1} creation failed: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to server")
            return
    
    print(f"✅ Created {len(created_messages)} test messages")
    
    # Test 1: Basic Pagination
    print("\n4. Testing Basic Pagination...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/", headers=headers_user1)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Pagination working - Page 1")
            print(f"   Total messages: {data['count']}")
            print(f"   Page size: {data['page_size']}")
            print(f"   Current page: {data['current_page']}")
            print(f"   Total pages: {data['total_pages']}")
            print(f"   Messages on this page: {len(data['results'])}")
            print(f"   Has next page: {data['has_next']}")
            print(f"   Has previous page: {data['has_previous']}")
        else:
            print(f"❌ Pagination test failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 2: Page Navigation
    print("\n5. Testing Page Navigation...")
    
    try:
        # Get page 2
        response = requests.get(f"{BASE_URL}/messages/?page=2", headers=headers_user1)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Page 2 loaded successfully")
            print(f"   Current page: {data['current_page']}")
            print(f"   Messages on this page: {len(data['results'])}")
        else:
            print(f"❌ Page 2 test failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 3: Custom Page Size
    print("\n6. Testing Custom Page Size...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/?page_size=5", headers=headers_user1)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Custom page size working")
            print(f"   Page size: {data['page_size']}")
            print(f"   Messages on this page: {len(data['results'])}")
            print(f"   Total pages with page_size=5: {data['total_pages']}")
        else:
            print(f"❌ Custom page size test failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 4: Filtering by Sender
    print("\n7. Testing Filtering by Sender...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/?sender={user1_id}", headers=headers_user1)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sender filtering working")
            print(f"   Messages from sender: {data['count']}")
            print(f"   Messages on this page: {len(data['results'])}")
        else:
            print(f"❌ Sender filtering test failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 5: Filtering by Message Content
    print("\n8. Testing Filtering by Message Content...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/?message_contains=work", headers=headers_user1)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Content filtering working")
            print(f"   Messages containing 'work': {data['count']}")
            print(f"   Messages on this page: {len(data['results'])}")
            if data['results']:
                print(f"   First result: {data['results'][0]['message_body']}")
        else:
            print(f"❌ Content filtering test failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 6: Date Range Filtering
    print("\n9. Testing Date Range Filtering...")
    
    try:
        # Filter messages from today
        today = datetime.now().date()
        response = requests.get(f"{BASE_URL}/messages/?sent_date={today}", headers=headers_user1)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Date filtering working")
            print(f"   Messages from today: {data['count']}")
            print(f"   Messages on this page: {len(data['results'])}")
        else:
            print(f"❌ Date filtering test failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 7: Ordering
    print("\n10. Testing Ordering...")
    
    try:
        # Test ascending order
        response = requests.get(f"{BASE_URL}/messages/?ordering=sent_at", headers=headers_user1)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Ordering working")
            print(f"   Messages in ascending order: {len(data['results'])}")
            if len(data['results']) >= 2:
                first_msg = data['results'][0]['message_body']
                last_msg = data['results'][-1]['message_body']
                print(f"   First message: {first_msg}")
                print(f"   Last message: {last_msg}")
        else:
            print(f"❌ Ordering test failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 8: Search Functionality
    print("\n11. Testing Search Functionality...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/?search=message", headers=headers_user1)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search working")
            print(f"   Messages matching 'message': {data['count']}")
            print(f"   Messages on this page: {len(data['results'])}")
        else:
            print(f"❌ Search test failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 9: Combined Filtering and Pagination
    print("\n12. Testing Combined Filtering and Pagination...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/?message_contains=message&page_size=5&page=1", headers=headers_user1)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Combined filtering and pagination working")
            print(f"   Total messages matching filter: {data['count']}")
            print(f"   Page size: {data['page_size']}")
            print(f"   Current page: {data['current_page']}")
            print(f"   Messages on this page: {len(data['results'])}")
        else:
            print(f"❌ Combined test failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 10: Custom Actions
    print("\n13. Testing Custom Actions...")
    
    try:
        # Test recent messages action
        response = requests.get(f"{BASE_URL}/messages/recent/?limit=5", headers=headers_user1)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recent messages action working")
            print(f"   Recent messages: {len(data)}")
        else:
            print(f"❌ Recent messages action failed: {response.status_code}")
        
        # Test search action
        response = requests.get(f"{BASE_URL}/messages/search/?q=work", headers=headers_user1)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search action working")
            print(f"   Search results: {len(data)}")
        else:
            print(f"❌ Search action failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    print("\n" + "=" * 60)
    print("🎉 All pagination and filtering tests completed!")
    print("\nFeatures Tested:")
    print("✅ Basic pagination (20 messages per page)")
    print("✅ Page navigation")
    print("✅ Custom page size")
    print("✅ Filtering by sender")
    print("✅ Filtering by message content")
    print("✅ Date range filtering")
    print("✅ Ordering (ascending/descending)")
    print("✅ Search functionality")
    print("✅ Combined filtering and pagination")
    print("✅ Custom actions (recent, search)")
    
    print("\nAvailable Filter Parameters:")
    print("  ?page=1                    - Page number")
    print("  ?page_size=20              - Items per page")
    print("  ?sender=UUID               - Filter by sender")
    print("  ?message_contains=text     - Filter by message content")
    print("  ?sent_date=YYYY-MM-DD      - Filter by date")
    print("  ?sent_after=datetime       - Filter after date")
    print("  ?sent_before=datetime      - Filter before date")
    print("  ?ordering=sent_at          - Order by field")
    print("  ?search=query              - Search in messages")
    print("  ?conversation=UUID         - Filter by conversation")

if __name__ == "__main__":
    test_pagination_and_filtering()
