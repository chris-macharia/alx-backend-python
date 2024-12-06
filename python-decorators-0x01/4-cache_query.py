import mysql.connector
import functools

# Cache dictionary to store query results
query_cache = {}

def cache_query(func):
    """Decorator to cache query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')  # Extract query from kwargs
        if not query:
            raise ValueError("Query parameter is missing")

        # Check if the query result is in the cache
        if query in query_cache:
            print("Cache hit: Returning cached result")
            return query_cache[query]

        # If not cached, execute the function and store the result
        print("Cache miss: Executing query and caching result")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result

    return wrapper

# Decorator to handle database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(
            host="localhost",     # Your MySQL host
            user="chris", # Your MySQL username
            password="D@tabreach2024", # Your MySQL password
            database="ALX_prodev"  # Your MySQL database name
        )

        try:
            # Pass the connection to the function
            result = func(*args, conn=conn, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            result = None
        finally:
            # Ensure the connection is closed
            conn.close()

        return result
    return wrapper

@with_db_connection
@cache_query
def execute_query(conn, query):
    """Execute the given SQL query and return the result."""
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Example usage
try:
    # First execution (cache miss)
    users = execute_query(query="SELECT * FROM user_data")
    print(users)

    # Second execution (cache hit)
    cached_users = execute_query(query="SELECT * FROM user_data")
    print(cached_users)
except Exception as e:
    print(f"Error: {e}")
