import mysql.connector
import functools

# Decorator to handle database connection
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

# Transaction management decorator
def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the connection object from the kwargs (passed by with_db_connection)
        conn = kwargs.get('conn')
        if not conn:
            raise ValueError("No database connection found")

        cursor = conn.cursor()
        
        try:
            # Begin transaction
            conn.start_transaction()

            # Run the actual database operation
            result = func(*args, **kwargs)

            # Commit the transaction if the operation succeeds
            conn.commit()
        except Exception as e:
            # Rollback in case of error
            print(f"Error: {e}")
            conn.rollback()
            result = None
        finally:
            # Closing the cursor after the operation
            cursor.close()

        return result
    return wrapper

# Example function using both decorators
@with_db_connection
@transactional
def add_user(conn,user_id, user_name, user_email, user_age):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)", (user_id, user_name, user_email, user_age))
    print("User added successfully")

# Example usage: Adding a new user with automatic transaction management
add_user(user_id="sm1001", user_name="Dorothy Vugutsa", user_email="doshvugutsa@example.com", user_age="21")
