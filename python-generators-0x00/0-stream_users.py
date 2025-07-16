#!/usr/bin/python3
"""
Generator function to stream users from the database one by one.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.
    
    Yields:
        dict: Dictionary containing user data (user_id, name, email, age)
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            
            # Use a single loop to fetch and yield rows one by one
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                yield row
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return 