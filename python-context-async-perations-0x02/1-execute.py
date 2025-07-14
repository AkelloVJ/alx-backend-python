import sqlite3

class ExecuteQuery:
    """Reusable context manager for executing database queries"""
    
    def __init__(self, query, params=None, database_path='users.db'):
        self.query = query
        self.params = params or ()
        self.database_path = database_path
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """Open database connection and execute query"""
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Use the context manager with the specified query and parameter
with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
    print(results) 