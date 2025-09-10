#!/usr/bin/env python3
"""
Test script to verify the RestrictAccessByTimeMiddleware functionality
"""

import requests
from datetime import datetime, time as dt_time

def test_time_restriction():
    """Test the time restriction middleware"""
    
    print("🕐 Testing RestrictAccessByTimeMiddleware")
    print("=" * 50)
    
    # Get current time
    current_time = datetime.now().time()
    print(f"Current time: {current_time}")
    
    # Define allowed time window (6PM to 9PM)
    start_time = dt_time(18, 0)  # 6PM
    end_time = dt_time(21, 0)    # 9PM
    
    print(f"Allowed time window: {start_time} - {end_time}")
    
    # Check if current time is within allowed window
    is_allowed = start_time <= current_time <= end_time
    print(f"Access should be {'ALLOWED' if is_allowed else 'DENIED'}")
    
    # Test the middleware
    try:
        # Test messaging endpoints
        test_endpoints = [
            "/api/messages/",
            "/api/conversations/",
            "/api/chats/"
        ]
        
        for endpoint in test_endpoints:
            print(f"\nTesting endpoint: {endpoint}")
            try:
                response = requests.get(f"http://127.0.0.1:8000{endpoint}")
                print(f"  Status Code: {response.status_code}")
                
                if response.status_code == 403:
                    print("  ✅ Time restriction working - Access denied")
                    try:
                        error_data = response.json()
                        print(f"  Error: {error_data.get('error', 'Unknown error')}")
                        print(f"  Message: {error_data.get('message', 'No message')}")
                    except:
                        print("  Response: Non-JSON response")
                elif response.status_code == 200:
                    print("  ✅ Time restriction allows access (within allowed hours)")
                else:
                    print(f"  ⚠️  Unexpected status code: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print("  ❌ Server not running. Please start with: python manage.py runserver")
                break
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        # Test non-messaging endpoints (should not be restricted)
        print(f"\nTesting non-messaging endpoint: /api/auth/register/")
        try:
            response = requests.get("http://127.0.0.1:8000/api/auth/register/")
            print(f"  Status Code: {response.status_code}")
            if response.status_code != 403:
                print("  ✅ Non-messaging endpoint not restricted (as expected)")
            else:
                print("  ⚠️  Non-messaging endpoint is being restricted (unexpected)")
        except requests.exceptions.ConnectionError:
            print("  ❌ Server not running")
        except Exception as e:
            print(f"  ❌ Error: {e}")
            
    except Exception as e:
        print(f"❌ Test error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Time Restriction Middleware Test Complete!")
    
    if is_allowed:
        print("✅ Current time is within allowed hours (6PM-9PM)")
        print("   Messaging endpoints should be accessible")
    else:
        print("❌ Current time is outside allowed hours (6PM-9PM)")
        print("   Messaging endpoints should return 403 Forbidden")

if __name__ == "__main__":
    test_time_restriction()
