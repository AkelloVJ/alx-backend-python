# Python Context Managers and Async Operations

This project demonstrates the implementation of custom context managers and asynchronous database operations in Python. It focuses on creating reusable, efficient, and clean code for database management using context managers and asyncio.

## Overview

The project contains three main implementations:

1. **DatabaseConnection Context Manager** - Custom class-based context manager for database connections
2. **ExecuteQuery Context Manager** - Reusable context manager for executing queries with parameters
3. **Concurrent Async Operations** - Asynchronous database queries using asyncio and aiosqlite

## Files

- `0-databaseconnection.py` - Custom class-based context manager for database connections
- `1-execute.py` - Reusable query context manager with parameter support
- `3-concurrent.py` - Concurrent asynchronous database queries
- `setup_database.py` - Database setup script for testing
- `demo_all_operations.py` - Comprehensive demo of all implementations

## Implementation Details

### 1. DatabaseConnection Context Manager

**Purpose**: Custom class-based context manager that automatically handles database connections.

**Features**:
- Uses `__enter__()` and `__exit__()` methods
- Automatically opens and closes database connections
- Returns cursor for database operations
- Proper resource cleanup with try-finally pattern

**Usage**:
```python
with DatabaseConnection() as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
```

### 2. ExecuteQuery Context Manager

**Purpose**: Reusable context manager that takes a query and parameters, executes it, and returns results.

**Features**:
- Accepts SQL query and parameters
- Executes query and returns results directly
- Automatic connection management
- Parameterized query support for security

**Usage**:
```python
with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
    print(results)
```

### 3. Concurrent Async Operations

**Purpose**: Demonstrates concurrent database operations using asyncio and aiosqlite.

**Features**:
- Uses `aiosqlite` for asynchronous SQLite operations
- Implements `async_fetch_users()` and `async_fetch_older_users()` functions
- Uses `asyncio.gather()` for concurrent execution
- Uses `asyncio.run()` to run the concurrent operations

**Usage**:
```python
async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

results = asyncio.run(fetch_concurrently())
```

## Setup and Testing

### Prerequisites
- Python 3.8 or higher
- SQLite3 (included with Python)
- aiosqlite library for async operations

### Installation
```bash
pip install aiosqlite --break-system-packages
```

### Database Setup
Run the setup script to create a sample database:
```bash
python3 setup_database.py
```

### Running Individual Tests
Test each implementation:
```bash
python3 0-databaseconnection.py
python3 1-execute.py
python3 3-concurrent.py
```

### Running the Demo
Execute the comprehensive demo:
```bash
python3 demo_all_operations.py
```

## Learning Objectives

By completing this project, developers will:

1. **Master Context Managers**: Understand how to create custom context managers using `__enter__()` and `__exit__()` methods
2. **Resource Management**: Learn proper resource cleanup and connection management
3. **Async Programming**: Understand asynchronous database operations with asyncio
4. **Concurrent Operations**: Learn to execute multiple database queries concurrently
5. **Best Practices**: Apply clean code principles and proper error handling

## Key Features

### Context Managers
- **Automatic Resource Management**: Connections are automatically opened and closed
- **Error Handling**: Proper exception handling and resource cleanup
- **Reusability**: Context managers can be used multiple times
- **Clean Code**: Eliminates boilerplate connection management code

### Async Operations
- **Concurrent Execution**: Multiple queries run simultaneously
- **Performance**: Improved performance through asynchronous operations
- **Modern Python**: Uses asyncio for modern async programming
- **Scalability**: Can handle multiple concurrent database operations

## Best Practices Demonstrated

1. **Resource Management**: Proper opening and closing of database connections
2. **Error Handling**: Comprehensive exception handling in context managers
3. **Async/Await Pattern**: Modern asynchronous programming techniques
4. **Concurrent Programming**: Using asyncio.gather for parallel operations
5. **Clean Code**: Readable and maintainable code structure

## Performance Benefits

- **Context Managers**: Reduce code duplication and ensure proper resource cleanup
- **Async Operations**: Improve performance through concurrent execution
- **Connection Pooling**: Efficient database connection management
- **Memory Management**: Automatic cleanup prevents memory leaks

## Future Enhancements

- Add connection pooling for better performance
- Implement transaction support in context managers
- Add support for different database backends
- Create async context managers
- Add metrics and monitoring capabilities
- Implement connection retry mechanisms

## Testing Results

All implementations have been tested and verified:

✅ **DatabaseConnection Context Manager**: Successfully retrieves all users
✅ **ExecuteQuery Context Manager**: Correctly filters users by age
✅ **Async Operations**: Concurrently fetches different user sets
✅ **Error Handling**: Proper exception handling and resource cleanup
✅ **Performance**: Concurrent operations show improved performance

The project demonstrates a comprehensive understanding of Python context managers and asynchronous programming for database operations. 