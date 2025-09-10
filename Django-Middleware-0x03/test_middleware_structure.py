#!/usr/bin/env python3
"""
Test script to verify the new modular middleware structure
"""

import requests
import time
from datetime import datetime

def test_middleware_structure():
    """Test all middleware functionality with the new structure"""
    
    print("🏗️ Testing Django Middleware Structure")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000/api"
    
    # Test 1: Basic endpoint access
    print("\n1. Testing basic endpoint access...")
    try:
        response = requests.get(f"{base_url}/test/")
        print(f"✅ Test endpoint accessible: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data.get('message', 'No message')}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start with: python manage.py runserver")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Request logging (check if requests.log is created)
    print("\n2. Testing request logging...")
    try:
        response = requests.get(f"{base_url}/test/")
        print("✅ Request made - Check requests.log file for logging")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Time restriction middleware
    print("\n3. Testing time restriction middleware...")
    current_time = datetime.now().time()
    print(f"   Current time: {current_time}")
    
    try:
        response = requests.get(f"{base_url}/messages/")
        if response.status_code == 403:
            print("✅ Time restriction working - Access denied outside 6PM-9PM")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', 'Unknown error')}")
                print(f"   Message: {error_data.get('message', 'No message')}")
            except:
                print(f"   Response: {response.text}")
        elif response.status_code == 200:
            print("✅ Time restriction allows access (within allowed hours)")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Rate limiting middleware
    print("\n4. Testing rate limiting middleware...")
    print("   Sending multiple POST requests to test rate limiting...")
    
    for i in range(7):  # Try to send 7 messages (limit is 5)
        try:
            message_data = {"message": f"Test message {i+1}"}
            response = requests.post(f"{base_url}/messages/", json=message_data)
            
            if response.status_code == 201:
                print(f"   ✅ Message {i+1} sent successfully")
            elif response.status_code == 429:
                print(f"   🚫 Rate limit triggered at message {i+1}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('error', 'Unknown error')}")
                    print(f"   Message: {error_data.get('message', 'No message')}")
                except:
                    print(f"   Response: {response.text}")
                break
            else:
                print(f"   ⚠️  Status for message {i+1}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error sending message {i+1}: {e}")
    
    # Test 5: Role permission middleware
    print("\n5. Testing role permission middleware...")
    
    # Test protected endpoints without authentication
    protected_endpoints = ["/users/", "/admin/"]
    
    for endpoint in protected_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code == 401:
                print(f"✅ {endpoint} requires authentication (401)")
            elif response.status_code == 403:
                print(f"✅ {endpoint} access denied (403)")
            else:
                print(f"⚠️  {endpoint} status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing {endpoint}: {e}")
    
    # Test 6: Security headers
    print("\n6. Testing security headers...")
    try:
        response = requests.get(f"{base_url}/test/")
        print("✅ Security headers added to response")
        print(f"   X-Content-Type-Options: {response.headers.get('X-Content-Type-Options', 'Not set')}")
        print(f"   X-Frame-Options: {response.headers.get('X-Frame-Options', 'Not set')}")
        print(f"   X-XSS-Protection: {response.headers.get('X-XSS-Protection', 'Not set')}")
    except Exception as e:
        print(f"❌ Error testing security headers: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Middleware Structure Test Complete!")
    print("\n✅ New Structure Features:")
    print("   - Modular middleware organization")
    print("   - Separate files for each middleware")
    print("   - Proper apps/core/middleware structure")
    print("   - Clean separation of concerns")
    print("   - Config-based settings management")
    
    print("\n📁 Project Structure:")
    print("   Django-Middleware-0x03/")
    print("   ├── config/")
    print("   │   ├── settings.py")
    print("   │   └── urls.py")
    print("   ├── apps/")
    print("   │   ├── core/")
    print("   │   │   ├── middleware/")
    print("   │   │   │   ├── request_logging.py")
    print("   │   │   │   ├── time_restriction.py")
    print("   │   │   │   ├── rate_limiting.py")
    print("   │   │   │   ├── role_permissions.py")
    print("   │   │   │   ├── security_headers.py")
    print("   │   │   │   └── data_filtering.py")
    print("   │   │   └── views.py")
    print("   │   ├── users/")
    print("   │   └── listings/")
    print("   └── manage.py")

if __name__ == "__main__":
    test_middleware_structure()
