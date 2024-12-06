import mysql.connector
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            print(f"Executing SQL Query: {query}")
        else:
            print("No SQL Query provided!")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = mysql.connector.connect(
        host="localhost",
        user="chris",
        password="D@tabreach2024",
        database="ALX_prodev"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM user_data")
print(users)
