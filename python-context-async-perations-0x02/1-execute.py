import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def __enter__(self):
        try:
            # Establish a database connection
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Connection established successfully.")
            return self.connection
        except Error as e:
            print(f"Error while connecting to database: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connection closed.")

# Usage example
if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "database": "ALX_prodev",
        "user": "chris",
        "password": "D@tabreach2024"
    }

    query = "SELECT * FROM user_data"

    try:
        with DatabaseConnection(**db_config) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            # Print the results
            for row in results:
                print(row)
    except Error as e:
        print(f"Database operation failed: {e}")
