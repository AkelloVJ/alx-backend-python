# Python Generators - Database Streaming

## Overview

This project demonstrates the use of Python generators to stream rows from an SQL database one by one, providing memory-efficient data processing for large datasets.

## Features

- **Database Setup**: MySQL database creation and table setup
- **Data Seeding**: CSV data import with duplicate prevention
- **Generator Functions**: Memory-efficient row streaming
- **Batch Processing**: Configurable batch size for different use cases

## Database Schema

The `ALX_prodev` database contains a `user_data` table with the following structure:

```sql
CREATE TABLE user_data (
    user_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL(5,2) NOT NULL,
    INDEX idx_user_id (user_id)
);
```

## Functions

### Core Database Functions

- `connect_db()`: Connects to MySQL server
- `create_database(connection)`: Creates ALX_prodev database
- `connect_to_prodev()`: Connects to ALX_prodev database
- `create_table(connection)`: Creates user_data table
- `insert_data(connection, data)`: Inserts CSV data into database

### Generator Functions

- `stream_users(connection)`: Streams users one by one
- `stream_users_batch(connection, batch_size)`: Streams users in batches

## Usage

### Basic Setup

```python
import seed

# Setup database
connection = seed.connect_db()
seed.create_database(connection)
connection.close()

# Connect to specific database
connection = seed.connect_to_prodev()
seed.create_table(connection)
seed.insert_data(connection, 'user_data.csv')
```

### Using Generators

```python
# Stream users one by one
for user in seed.stream_users(connection):
    print(f"Processing user: {user}")
    # Process each user individually

# Stream users in batches
for batch in seed.stream_users_batch(connection, batch_size=100):
    print(f"Processing batch of {len(batch)} users")
    # Process batch of users
```

### Running the Example

```bash
# Make the main script executable
chmod +x 0-main.py

# Run the example
./0-main.py
```

## Requirements

- Python 3.6+
- MySQL Server
- mysql-connector-python

## Installation

```bash
pip install mysql-connector-python
```

## Benefits of Generators

1. **Memory Efficiency**: Only loads one row at a time into memory
2. **Scalability**: Can handle large datasets without memory issues
3. **Lazy Evaluation**: Processes data only when needed
4. **Batch Processing**: Configurable batch sizes for different use cases

## Example Output

```
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ...]

Testing generator function:
Generated user 1: ('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67)
Generated user 2: ('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119)
Generated user 3: ('006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49)
```

## Error Handling

The code includes comprehensive error handling for:
- Database connection failures
- Table creation errors
- Data insertion issues
- CSV file not found
- Generator streaming errors

## Performance Considerations

- Use appropriate batch sizes based on available memory
- Consider indexing strategies for large datasets
- Monitor database connection pool usage
- Implement connection pooling for production use 