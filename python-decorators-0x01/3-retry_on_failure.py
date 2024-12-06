import mysql.connector
import functools
import time

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

# Retry decorator
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    # Attempt to execute the function
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt >= retries:
                        print("Max retries reached. Operation failed.")
                        raise  # Re-raise the exception if max retries are reached
                    else:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)  # Wait before retrying
        return wrapper
    return decorator

# Example function using both decorators
@with_db_connection
@retry_on_failure(retries=3, delay=2)
def add_user(conn, user_id, user_name, user_email, user_age):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
        (user_id, user_name, user_email, user_age)
    )
    conn.commit()  # Commit the transaction
    print("User added successfully")
    cursor.close()

# Example usage: Adding a new user with retry logic
try:
    add_user(user_id="SM10002", user_name="Jackline Wavinya", user_email="jackiewakavinye@example.com", user_age=20)
except Exception as e:
    print(f"Final error: {e}")
