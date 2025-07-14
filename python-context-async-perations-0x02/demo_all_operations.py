#!/usr/bin/env python3
"""
Comprehensive demo of Context Managers and Async Operations
Shows all implementations working together
"""

import asyncio
import aiosqlite
import sqlite3
import time

# Import context managers
from importlib import import_module
import sys
sys.path.append('.')

def create_sample_database():
    """Create a sample users database for testing"""
    import os
    
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
        (3, 'Bob Johnson', 'bob.johnson@example.com', 45),
        (4, 'Alice Brown', 'alice.brown@example.com', 28),
        (5, 'Charlie Wilson', 'charlie.wilson@example.com', 50),
        (6, 'Diana Davis', 'diana.davis@example.com', 22),
        (7, 'Eve Miller', 'eve.miller@example.com', 55)
    ]
    
    cursor.executemany('INSERT INTO users (id, name, email, age) VALUES (?, ?, ?, ?)', sample_users)
    conn.commit()
    conn.close()
    print("✅ Sample database created successfully!")

# Define context managers for demo
class DatabaseConnection:
    """Custom context manager for database connections"""
    
    def __init__(self, database_path='users.db'):
        self.database_path = database_path
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """Open database connection and return cursor"""
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

class ExecuteQuery:
    """Reusable context manager for executing database queries"""
    
    def __init__(self, query, params=None, database_path='users.db'):
        self.query = query
        self.params = params or ()
        self.database_path = database_path
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """Open database connection and execute query"""
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Async functions
async def async_fetch_users():
    """Fetch all users asynchronously"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            return results

async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            return results

async def fetch_concurrently():
    """Execute both queries concurrently using asyncio.gather"""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

def demo_context_managers():
    """Demonstrate context managers"""
    print("🔧 Testing Context Managers")
    print("=" * 40)
    
    # Demo 1: DatabaseConnection context manager
    print("\n1️⃣  Testing DatabaseConnection Context Manager:")
    try:
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            print(f"✅ Retrieved {len(results)} users using DatabaseConnection")
            print(f"📊 Sample data: {results[:2]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Demo 2: ExecuteQuery context manager
    print("\n2️⃣  Testing ExecuteQuery Context Manager:")
    try:
        with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
            print(f"✅ Retrieved {len(results)} users older than 25")
            print(f"📊 Users older than 25: {results}")
    except Exception as e:
        print(f"❌ Error: {e}")

async def demo_async_operations():
    """Demonstrate async operations"""
    print("\n3️⃣  Testing Async Operations:")
    try:
        start_time = time.time()
        results = await fetch_concurrently()
        end_time = time.time()
        
        all_users, older_users = results
        print(f"✅ Retrieved {len(all_users)} total users")
        print(f"✅ Retrieved {len(older_users)} users older than 40")
        print(f"⏱️  Concurrent execution time: {end_time - start_time:.4f} seconds")
        print(f"📊 Users older than 40: {older_users}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main demo function"""
    print("🚀 Starting Context Managers and Async Operations Demo")
    print("=" * 60)
    
    # Create database
    create_sample_database()
    
    # Demo context managers
    demo_context_managers()
    
    # Demo async operations
    asyncio.run(demo_async_operations())
    
    print("\n🎉 Demo completed successfully!")

if __name__ == "__main__":
    main() 