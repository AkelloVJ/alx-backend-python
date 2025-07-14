import time
import sqlite3 
import functools

query_cache = {}

def with_db_connection(func):
    """Decorator to automatically handle database connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection as the first argument to the function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """Decorator to cache query results based on SQL query string"""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Use the query as the cache key
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]
        
        # Execute the query and cache the result
        print(f"Executing query and caching result: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users") 