#!/usr/bin/python3
"""
Batch processing functions for large data sets.
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows in batches from the user_data table.
    
    Args:
        batch_size (int): Number of rows to fetch in each batch
        
    Yields:
        list: List of dictionaries containing user data
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
            offset = 0
            
            # Loop 1: Fetch batches of data
            while True:
                cursor.execute(
                    "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
                    (batch_size, offset)
                )
                
                rows = cursor.fetchall()
                if not rows:
                    break
                    
                yield rows
                offset += batch_size
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.
    
    Args:
        batch_size (int): Number of rows to process in each batch
    """
    # Loop 2: Iterate over batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: Process each user in the batch
        for user in batch:
            if user['age'] > 25:
                print(user) 