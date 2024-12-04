import mysql.connector

def stream_users():
    """
    Generator function to fetch rows one by one from the user_data table in a MySQL database.
    Yields:
        tuple: A row from the user_data table.
    """
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host="localhost",        # e.g., "localhost"
        user="chris",    # e.g., "root"
        password="D@tabreach2024", # Your MySQL password
        database="ALX_prodev" # The database containing the user_data table
    )
    cursor = connection.cursor()

    try:
        # Execute the query to fetch all rows from the user_data table
        cursor.execute("SELECT * FROM user_data")
        
        # Use a single loop to yield rows one by one
        for row in cursor:
            yield row

    finally:
        # Always close the cursor and connection
        cursor.close()
        connection.close()
