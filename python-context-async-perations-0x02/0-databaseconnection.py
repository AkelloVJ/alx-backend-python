import sqlite3

class DatabaseConnection:
    """Custom context manager for database connections"""
    
    def __init__(self, database_path='users.db'):
        self.database_path = database_path
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """Open database connection and return cursor"""
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Use the context manager to perform the query
with DatabaseConnection() as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results) 