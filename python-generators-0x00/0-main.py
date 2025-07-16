#!/usr/bin/python3
"""
Main script to test the database setup and generator functionality.
"""

seed = __import__('seed')

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print(f"connection successful")

    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')
        cursor = connection.cursor()
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present ")
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()
        
        # Test the generator function
        print("\nTesting generator function:")
        user_generator = seed.stream_users(connection)
        for i, user in enumerate(user_generator):
            if i < 3:  # Only show first 3 users
                print(f"Generated user {i+1}: {user}")
            else:
                break
        
        connection.close() 