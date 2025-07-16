#!/usr/bin/python3
"""
Memory-efficient aggregation using generators to calculate average age.
"""

import seed


def stream_user_ages():
    """
    Generator function that yields user ages one by one.
    
    Yields:
        float: User age from the database
    """
    try:
        connection = seed.connect_to_prodev()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT age FROM user_data")
            
            # Loop 1: Stream ages one by one
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                yield row[0]  # Yield the age value
            
            cursor.close()
            connection.close()
            
    except Exception as e:
        print(f"Error streaming user ages: {e}")
        return


def calculate_average_age():
    """
    Calculates the average age using the generator without loading entire dataset into memory.
    
    Returns:
        float: Average age of all users
    """
    total_age = 0
    count = 0
    
    # Loop 2: Process each age from the generator
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0
    
    average_age = total_age / count
    print(f"Average age of users: {average_age}")
    return average_age


if __name__ == "__main__":
    calculate_average_age() 