# Python Decorators for Database Operations

This project demonstrates the implementation of Python decorators to enhance database operations in Python applications. The decorators provide reusable, efficient, and clean code for common database tasks.

## Overview

The project contains five main decorators that address different aspects of database management:

1. **Logging Decorator** - Logs SQL queries before execution
2. **Connection Decorator** - Automatically handles database connections
3. **Transaction Decorator** - Manages database transactions with commit/rollback
4. **Retry Decorator** - Retries failed database operations
5. **Cache Decorator** - Caches query results to avoid redundant calls

## Files

- `0-log_queries.py` - Logging decorator implementation
- `1-with_db_connection.py` - Database connection decorator
- `2-transactional.py` - Transaction management decorator
- `3-retry_on_failure.py` - Retry mechanism decorator
- `4-cache_query.py` - Query caching decorator
- `test_decorators.py` - Database setup script
- `demo_all_decorators.py` - Comprehensive demo of all decorators

## Decorator Details

### 1. Logging Decorator (`log_queries`)

**Purpose**: Logs SQL queries before execution for debugging and monitoring.

**Usage**:
```python
@log_queries
def fetch_all_users(query):
    # Database operations
    return results
```

**Features**:
- Extracts query from function arguments
- Prints query before execution
- Works with both positional and keyword arguments

### 2. Connection Decorator (`with_db_connection`)

**Purpose**: Automatically handles database connections, eliminating boilerplate code.

**Usage**:
```python
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()
```

**Features**:
- Opens connection before function execution
- Passes connection as first argument to decorated function
- Automatically closes connection after function completion
- Uses try-finally to ensure connection cleanup

### 3. Transaction Decorator (`transactional`)

**Purpose**: Manages database transactions with automatic commit/rollback.

**Usage**:
```python
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
```

**Features**:
- Automatically commits successful transactions
- Rolls back failed transactions
- Provides error handling and logging
- Works with the connection decorator

### 4. Retry Decorator (`retry_on_failure`)

**Purpose**: Retries database operations on failure to handle transient errors.

**Usage**:
```python
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
```

**Features**:
- Configurable number of retry attempts
- Configurable delay between retries
- Logs retry attempts
- Raises final exception if all retries fail

### 5. Cache Decorator (`cache_query`)

**Purpose**: Caches query results to avoid redundant database calls.

**Usage**:
```python
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()
```

**Features**:
- Uses query string as cache key
- Returns cached results for identical queries
- Logs cache hits and misses
- Global cache dictionary for session persistence

## Setup and Testing

### Prerequisites
- Python 3.8 or higher
- SQLite3 (included with Python)

### Database Setup
Run the test script to create a sample database:
```bash
python3 test_decorators.py
```

### Running the Demo
Execute the comprehensive demo to see all decorators in action:
```bash
python3 demo_all_decorators.py
```

### Testing Individual Decorators
Each decorator can be tested individually:
```bash
python3 0-log_queries.py
python3 1-with_db_connection.py
python3 2-transactional.py
python3 3-retry_on_failure.py
python3 4-cache_query.py
```

## Learning Objectives

By completing this project, developers will:

1. **Deepen Python Decorator Knowledge**: Understand how decorators work and their applications
2. **Enhance Database Management**: Automate repetitive database tasks
3. **Implement Robust Error Handling**: Build resilient database operations
4. **Optimize Performance**: Use caching to reduce redundant database calls
5. **Apply Best Practices**: Create scalable and maintainable database code

## Key Features

- **Modular Design**: Each decorator is self-contained and reusable
- **Error Handling**: Comprehensive exception handling and logging
- **Performance Optimization**: Caching and connection pooling
- **Clean Code**: Eliminates boilerplate and repetitive code
- **Real-world Application**: Simulates actual database management scenarios

## Best Practices Demonstrated

1. **Separation of Concerns**: Each decorator handles one specific aspect
2. **Error Handling**: Proper exception handling and cleanup
3. **Resource Management**: Automatic connection and transaction management
4. **Logging**: Comprehensive logging for debugging and monitoring
5. **Performance**: Caching and retry mechanisms for optimization

## Future Enhancements

- Add connection pooling for better performance
- Implement cache expiration mechanisms
- Add support for different database backends
- Create decorator composition utilities
- Add metrics and monitoring capabilities 