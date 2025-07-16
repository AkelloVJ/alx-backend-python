#!/usr/bin/python3
"""
Lazy pagination implementation using generators.
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database.
    
    Args:
        page_size (int): Number of users per page
        offset (int): Offset for pagination
        
    Returns:
        list: List of user dictionaries
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator function that implements lazy pagination.
    Only fetches the next page when needed, starting at offset 0.
    
    Args:
        page_size (int): Number of users per page
        
    Yields:
        list: List of user dictionaries for each page
    """
    offset = 0
    
    # Only one loop as required
    while True:
        page = paginate_users(page_size, offset)
        
        # If no more data, break the loop
        if not page:
            break
            
        yield page
        offset += page_size 