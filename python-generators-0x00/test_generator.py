#!/usr/bin/python3
"""
Test script to demonstrate the generator functionality.
"""

import seed

def test_single_user_streaming():
    """Test streaming users one by one."""
    print("=== Testing Single User Streaming ===")
    
    connection = seed.connect_to_prodev()
    if not connection:
        print("Failed to connect to database")
        return
    
    try:
        user_count = 0
        for user in seed.stream_users(connection):
            user_count += 1
            if user_count <= 3:
                print(f"User {user_count}: {user}")
            elif user_count == 4:
                print("... (showing only first 3 users)")
                break
        
        print(f"Total users in database: {user_count}")
        
    finally:
        connection.close()

def test_batch_streaming():
    """Test streaming users in batches."""
    print("\n=== Testing Batch Streaming ===")
    
    connection = seed.connect_to_prodev()
    if not connection:
        print("Failed to connect to database")
        return
    
    try:
        batch_count = 0
        total_users = 0
        
        for batch in seed.stream_users_batch(connection, batch_size=3):
            batch_count += 1
            total_users += len(batch)
            print(f"Batch {batch_count}: {len(batch)} users")
            print(f"  Users: {batch}")
            
            if batch_count >= 2:  # Only show first 2 batches
                break
        
        print(f"Processed {batch_count} batches, {total_users} total users")
        
    finally:
        connection.close()

def test_generator_memory_efficiency():
    """Demonstrate memory efficiency of generators."""
    print("\n=== Testing Memory Efficiency ===")
    
    connection = seed.connect_to_prodev()
    if not connection:
        print("Failed to connect to database")
        return
    
    try:
        # This would use a lot of memory if we loaded all users at once
        # Instead, we process them one by one
        print("Processing users with generator (memory efficient):")
        
        processed_count = 0
        for user in seed.stream_users(connection):
            processed_count += 1
            # Simulate some processing
            user_id, name, email, age = user
            if processed_count <= 2:
                print(f"  Processing: {name} ({email}) - Age: {age}")
        
        print(f"Successfully processed {processed_count} users without loading all into memory")
        
    finally:
        connection.close()

if __name__ == "__main__":
    print("Python Generators - Database Streaming Demo")
    print("=" * 50)
    
    test_single_user_streaming()
    test_batch_streaming()
    test_generator_memory_efficiency()
    
    print("\n" + "=" * 50)
    print("Demo completed successfully!") 