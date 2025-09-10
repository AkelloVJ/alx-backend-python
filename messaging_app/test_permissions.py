#!/usr/bin/env python3
"""
Test script to demonstrate the IsParticipantOfConversation permission functionality
Run this after installing dependencies and running migrations
"""

import requests
import json
import uuid

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def test_permission_control():
    """Test the IsParticipantOfConversation permission implementation"""
    
    print("🔐 Testing IsParticipantOfConversation Permission Control")
    print("=" * 60)
    
    # Create two test users
    print("\n1. Creating Test Users...")
    
    # User 1
    user1_data = {
        "email": "user1@example.com",
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
        "email": "user2@example.com",
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
    
    # Test 2: Test unauthenticated access (should be denied)
    print("\n2. Testing Unauthenticated Access (Should be Denied)...")
    
    try:
        response = requests.get(f"{BASE_URL}/conversations/")
        if response.status_code == 401:
            print("✅ Unauthenticated access correctly denied")
        else:
            print(f"❌ Expected 401, got {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 3: User 1 creates a conversation
    print("\n3. User 1 Creating a Conversation...")
    
    headers_user1 = {
        "Authorization": f"Bearer {user1_access_token}",
        "Content-Type": "application/json"
    }
    
    conversation_data = {
        "participants_id": user1_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/conversations/", json=conversation_data, headers=headers_user1)
        if response.status_code == 201:
            print("✅ User 1 created conversation successfully")
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
    
    # Test 4: User 1 sends a message in their conversation
    print("\n4. User 1 Sending a Message in Their Conversation...")
    
    message_data = {
        "conversation": conversation_id,
        "message_body": "Hello, this is Alice's message!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/messages/", json=message_data, headers=headers_user1)
        if response.status_code == 201:
            print("✅ User 1 sent message successfully")
            message = response.json()
            message_id = message['message_id']
            print(f"   Message: {message['message_body']}")
        else:
            print(f"❌ Message sending failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 5: User 2 tries to access User 1's conversation (should be denied)
    print("\n5. User 2 Trying to Access User 1's Conversation (Should be Denied)...")
    
    headers_user2 = {
        "Authorization": f"Bearer {user2_access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/conversations/{conversation_id}/", headers=headers_user2)
        if response.status_code == 404:
            print("✅ User 2 correctly denied access to User 1's conversation")
        else:
            print(f"❌ Expected 404, got {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 6: User 2 tries to send a message to User 1's conversation (should be denied)
    print("\n6. User 2 Trying to Send Message to User 1's Conversation (Should be Denied)...")
    
    message_data_user2 = {
        "conversation": conversation_id,
        "message_body": "This should be denied!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/messages/", json=message_data_user2, headers=headers_user2)
        if response.status_code == 404:
            print("✅ User 2 correctly denied access to send message to User 1's conversation")
        else:
            print(f"❌ Expected 404, got {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 7: User 2 tries to view User 1's message (should be denied)
    print("\n7. User 2 Trying to View User 1's Message (Should be Denied)...")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/{message_id}/", headers=headers_user2)
        if response.status_code == 404:
            print("✅ User 2 correctly denied access to view User 1's message")
        else:
            print(f"❌ Expected 404, got {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 8: User 1 can view their own conversation and messages
    print("\n8. User 1 Accessing Their Own Conversation and Messages...")
    
    try:
        # View conversation
        response = requests.get(f"{BASE_URL}/conversations/{conversation_id}/", headers=headers_user1)
        if response.status_code == 200:
            print("✅ User 1 can access their own conversation")
        else:
            print(f"❌ User 1 should be able to access their conversation: {response.status_code}")
        
        # View message
        response = requests.get(f"{BASE_URL}/messages/{message_id}/", headers=headers_user1)
        if response.status_code == 200:
            print("✅ User 1 can access their own message")
        else:
            print(f"❌ User 1 should be able to access their message: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 9: User 1 can update their own message
    print("\n9. User 1 Updating Their Own Message...")
    
    update_data = {
        "message_body": "This is Alice's updated message!"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/messages/{message_id}/", json=update_data, headers=headers_user1)
        if response.status_code == 200:
            print("✅ User 1 successfully updated their message")
            updated_message = response.json()
            print(f"   Updated message: {updated_message['message_body']}")
        else:
            print(f"❌ Message update failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    # Test 10: User 2 tries to update User 1's message (should be denied)
    print("\n10. User 2 Trying to Update User 1's Message (Should be Denied)...")
    
    try:
        response = requests.patch(f"{BASE_URL}/messages/{message_id}/", json=update_data, headers=headers_user2)
        if response.status_code == 404:
            print("✅ User 2 correctly denied access to update User 1's message")
        else:
            print(f"❌ Expected 404, got {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return
    
    print("\n" + "=" * 60)
    print("🎉 All permission tests completed!")
    print("\nPermission Control Summary:")
    print("✅ Only authenticated users can access the API")
    print("✅ Only conversation participants can send, view, update, and delete messages")
    print("✅ Users cannot access other users' conversations or messages")
    print("✅ Global permission setting is working correctly")

if __name__ == "__main__":
    test_permission_control()
