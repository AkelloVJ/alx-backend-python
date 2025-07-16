#!/usr/bin/python3
"""
Database setup and data seeding script for ALX_prodev database.
Includes a generator function to stream rows from the database.
"""

import mysql.connector
import csv
import uuid
from typing import Generator, Tuple, Any


def connect_db():
    """
    Connects to the MySQL database server.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
        print("Database ALX_prodev created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev database: {err}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")


def insert_data(connection, data):
    """
    Inserts data in the database if it does not exist.
    
    Args:
        connection: MySQL connection object
        data (str): Path to the CSV file containing user data
    """
    try:
        cursor = connection.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("Data already exists in the database")
            cursor.close()
            return
        
        # Read CSV file and insert data
        with open(data, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Generate UUID if not present
                user_id = row.get('user_id') or str(uuid.uuid4())
                
                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    user_id,
                    row['name'],
                    row['email'],
                    row['age']
                ))
        
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
        
    except FileNotFoundError:
        print(f"CSV file {data} not found")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")


def stream_users(connection) -> Generator[Tuple[Any, ...], None, None]:
    """
    Generator function that streams rows from the user_data table one by one.
    
    Args:
        connection: MySQL connection object
        
    Yields:
        Tuple: Row data from the database
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
            
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")


def stream_users_batch(connection, batch_size: int = 100) -> Generator[list, None, None]:
    """
    Generator function that streams rows from the user_data table in batches.
    
    Args:
        connection: MySQL connection object
        batch_size (int): Number of rows to fetch in each batch
        
    Yields:
        list: Batch of row data from the database
    """
    try:
        cursor = connection.cursor()
        offset = 0
        
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
    except mysql.connector.Error as err:
        print(f"Error streaming data in batches: {err}")


if __name__ == "__main__":
    # Example usage of the generator
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
        
        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection, 'user_data.csv')
            
            # Example: Stream users one by one
            print("\nStreaming users one by one:")
            for user in stream_users(connection):
                print(f"User: {user}")
            
            # Example: Stream users in batches
            print("\nStreaming users in batches:")
            for batch in stream_users_batch(connection, batch_size=5):
                print(f"Batch: {batch}")
            
            connection.close() 