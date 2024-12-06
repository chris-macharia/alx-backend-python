import mysql.connector
import functools

# Decorator to handle database connection for MySQL
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Establishing the MySQL connection
        conn = mysql.connector.connect(
            host="localhost",     # Your MySQL host
            user="chris", # Your MySQL username
            password="D@tabreach2024", # Your MySQL password
            database="ALX_prodev"  # Your MySQL database name
        )

        try:
            # Passing the connection to the function
            result = func(*args, conn=conn, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            result = None
        finally:
            # Ensure the connection is closed after the function execution
            conn.close()

        return result
    return wrapper

# Function to get user by ID using the decorator
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
