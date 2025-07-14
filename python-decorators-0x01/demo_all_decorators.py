#!/usr/bin/env python3
"""
Comprehensive demo of all Python decorators
Shows how all decorators work together
"""

import sqlite3
import functools
import time
import os

# Import all decorators from the individual files
from importlib import import_module
import sys
sys.path.append('.')

# Create sample database first
def create_sample_database():
    """Create a sample users database for testing"""
    if os.path.exists('users.db'):
        os.remove('users.db')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        )
    ''')
    
    sample_users = [
        (1, 'John Doe', 'john.doe@example.com', 30),
        (2, 'Jane Smith', 'jane.smith@example.com', 25),
        (3, 'Bob Johnson', 'bob.johnson@example.com', 35),
        (4, 'Alice Brown', 'alice.brown@example.com', 28)
    ]
    
    cursor.executemany('INSERT INTO users (id, name, email, age) VALUES (?, ?, ?, ?)', sample_users)
    conn.commit()
    conn.close()
    print("✅ Sample database created successfully!")

# Define all decorators in one place for demo
def log_queries(func):
    """Decorator to log SQL queries before execution"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query', '')
        if not query and args:
            query = args[0] if isinstance(args[0], str) else ''
        print(f"🔍 Executing query: {query}")
        return func(*args, **kwargs)
    return wrapper

def with_db_connection(func):
    """Decorator to automatically handle database connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def transactional(func):
    """Decorator to manage database transactions"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("✅ Transaction committed successfully")
            return result
        except Exception as e:
            conn.rollback()
            print(f"❌ Transaction rolled back due to error: {e}")
            raise e
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """Decorator to retry database operations on failure"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < retries - 1:
                        print(f"⚠️  Attempt {attempt + 1} failed, retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"❌ All {retries} attempts failed")
            
            raise last_exception
        return wrapper
    return decorator

query_cache = {}

def cache_query(func):
    """Decorator to cache query results based on SQL query string"""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print(f"💾 Using cached result for query: {query}")
            return query_cache[query]
        
        print(f"🔄 Executing query and caching result: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# Demo functions using the decorators
@log_queries
@with_db_connection
def fetch_all_users(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"📧 Updated email for user {user_id} to {new_email}")

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def demo_all_decorators():
    """Demonstrate all decorators working together"""
    print("🚀 Starting Python Decorators Demo")
    print("=" * 50)
    
    # Demo 1: Logging decorator
    print("\n1️⃣  Testing Logging Decorator:")
    try:
        users = fetch_all_users(query="SELECT * FROM users")
        print(f"✅ Retrieved {len(users)} users")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Demo 2: Transaction decorator
    print("\n2️⃣  Testing Transaction Decorator:")
    try:
        update_user_email(user_id=1, new_email='john.updated@example.com')
        print("✅ Email update successful")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Demo 3: Retry decorator
    print("\n3️⃣  Testing Retry Decorator:")
    try:
        users = fetch_users_with_retry()
        print(f"✅ Retrieved {len(users)} users with retry mechanism")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Demo 4: Cache decorator
    print("\n4️⃣  Testing Cache Decorator:")
    try:
        # First call - should execute and cache
        users1 = fetch_users_with_cache(query="SELECT * FROM users")
        print(f"✅ First call: Retrieved {len(users1)} users")
        
        # Second call - should use cache
        users2 = fetch_users_with_cache(query="SELECT * FROM users")
        print(f"✅ Second call: Retrieved {len(users2)} users (from cache)")
        
        # Different query - should execute again
        users3 = fetch_users_with_cache(query="SELECT name, email FROM users")
        print(f"✅ Different query: Retrieved {len(users3)} users")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎉 Demo completed successfully!")

if __name__ == "__main__":
    create_sample_database()
    demo_all_decorators() 