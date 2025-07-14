#!/usr/bin/env python3
"""
Test script for Python decorators
Creates a sample database and tests all decorators
"""

import sqlite3
import os

def create_sample_database():
    """Create a sample users database for testing"""
    # Remove existing database if it exists
    if os.path.exists('users.db'):
        os.remove('users.db')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        )
    ''')
    
    # Insert sample data
    sample_users = [
        (1, 'John Doe', 'john.doe@example.com', 30),
        (2, 'Jane Smith', 'jane.smith@example.com', 25),
        (3, 'Bob Johnson', 'bob.johnson@example.com', 35),
        (4, 'Alice Brown', 'alice.brown@example.com', 28)
    ]
    
    cursor.executemany('INSERT INTO users (id, name, email, age) VALUES (?, ?, ?, ?)', sample_users)
    conn.commit()
    conn.close()
    print("Sample database created successfully!")

if __name__ == "__main__":
    create_sample_database()
    print("Database setup complete. You can now test the decorators!") 