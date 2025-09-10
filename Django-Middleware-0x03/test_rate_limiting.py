#!/usr/bin/env python3
"""
Test script to verify the OffensiveLanguageMiddleware (Rate Limiting) functionality
"""

import requests
import json
import time
from datetime import datetime

def test_rate_limiting():
    """Test the rate limiting middleware"""
    
    print("🚫 Testing OffensiveLanguageMiddleware (Rate Limiting)")
    print("=" * 60)
    
    # First, register and login a user
    print("1. Setting up test user...")
    
    user_data = {
        "email": f"ratetest{int(time.time())}@example.com",
        "password": "testpassword123",
        "first_name": "Rate",
        "last_name": "Test",
        "phone_number": "+1234567890",
        "role": "guest"
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/api/auth/register/", json=user_data)
        if response.status_code == 201:
            print("✅ User registered successfully")
            user_info = response.json()
            access_token = user_info['access']
            user_id = user_info['user']['user_id']
        else:
            print(f"❌ User registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start with: python manage.py runserver")
        return
    except Exception as e:
        print(f"❌ User registration error: {e}")
        return
    
    # Create a conversation for testing
    print("\n2. Creating test conversation...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        conversation_data = {"participants_id": user_id}
        response = requests.post("http://127.0.0.1:8000/api/conversations/", json=conversation_data, headers=headers)
        if response.status_code == 201:
            conversation = response.json()
            conversation_id = conversation['conversation_id']
            print("✅ Conversation created successfully")
        else:
            print(f"❌ Conversation creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Conversation creation error: {e}")
        return
    
    # Test rate limiting by sending multiple messages
    print("\n3. Testing rate limiting (5 messages per minute)...")
    print("   Sending 7 messages to test rate limit...")
    
    success_count = 0
    rate_limited = False
    
    for i in range(7):  # Try to send 7 messages (limit is 5)
        message_data = {
            "conversation": conversation_id,
            "message_body": f"Rate limit test message {i+1}"
        }
        
        try:
            print(f"   Sending message {i+1}...")
            response = requests.post("http://127.0.0.1:8000/api/messages/", json=message_data, headers=headers)
            
            if response.status_code == 201:
                success_count += 1
                print(f"   ✅ Message {i+1} sent successfully")
            elif response.status_code == 429:
                print(f"   🚫 Rate limit triggered at message {i+1}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('error', 'Unknown error')}")
                    print(f"   Message: {error_data.get('message', 'No message')}")
                    print(f"   Retry after: {error_data.get('retry_after', 'Unknown')} seconds")
                except:
                    print(f"   Response: {response.text}")
                rate_limited = True
                break
            else:
                print(f"   ❌ Unexpected status for message {i+1}: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Error sending message {i+1}: {e}")
    
    # Test non-message POST requests (should not be rate limited)
    print("\n4. Testing non-message POST requests (should not be rate limited)...")
    
    try:
        # Try to create another conversation (should not be rate limited)
        conversation_data2 = {"participants_id": user_id}
        response = requests.post("http://127.0.0.1:8000/api/conversations/", json=conversation_data2, headers=headers)
        if response.status_code in [201, 400]:  # 201 for success, 400 for duplicate
            print("✅ Non-message POST request not rate limited (as expected)")
        else:
            print(f"⚠️  Non-message POST request status: {response.status_code}")
    except Exception as e:
        print(f"❌ Non-message POST test error: {e}")
    
    # Test GET requests (should not be rate limited)
    print("\n5. Testing GET requests (should not be rate limited)...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/api/messages/", headers=headers)
        if response.status_code == 200:
            print("✅ GET requests not rate limited (as expected)")
        else:
            print(f"⚠️  GET request status: {response.status_code}")
    except Exception as e:
        print(f"❌ GET request test error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 Rate Limiting Test Results:")
    print(f"   Messages sent successfully: {success_count}")
    print(f"   Rate limit triggered: {'Yes' if rate_limited else 'No'}")
    
    if success_count == 5 and rate_limited:
        print("✅ Rate limiting working correctly!")
        print("   - Allowed 5 messages as configured")
        print("   - Blocked 6th message with 429 status")
    elif success_count < 5:
        print("⚠️  Rate limiting may be too restrictive")
    elif success_count > 5:
        print("❌ Rate limiting not working - too many messages allowed")
    else:
        print("ℹ️  Rate limiting test completed")

if __name__ == "__main__":
    test_rate_limiting()
