import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator function to fetch rows in batches from the user_data table.
    Args:
        batch_size (int): The size of each batch.
    Yields:
        list: A batch of rows from the user_data table.
    """
    connection = mysql.connector.connect(
        host="localhost",        # e.g., "localhost"
        user="chris",    # e.g., "root"
        password="D@tabreach2024",# Your MySQL password
        database="ALX_prodev" # The database containing the user_data table
    )
    cursor = connection.cursor(dictionary=True)

    try:
        # Execute a query to fetch all rows from the user_data table
        cursor.execute("SELECT * FROM user_data")
        while True:
            # Fetch the next batch of rows
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break  # Exit the loop if no more rows are fetched
            yield batch
    finally:
        # Always close the cursor and connection
        cursor.close()
        connection.close()

def batch_processing(batch_size):
    """
    Generator function to process each batch and filter users over the age of 25.
    Args:
        batch_size (int): The size of each batch.
    Yields:
        list: A batch of filtered users (age > 25).
    """
    for batch in stream_users_in_batches(batch_size):
        # Filter users over the age of 25
        filtered_batch = [user for user in batch if user['age'] > 25]
        yield filtered_batch
