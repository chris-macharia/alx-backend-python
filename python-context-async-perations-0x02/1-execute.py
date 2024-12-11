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

class ExecuteQuery:
    def __init__(self, connection, query, params):
        self.connection = connection
        self.query = query
        self.params = params
        self.results = None

    def __enter__(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(self.query, self.params)
            self.results = cursor.fetchall()
            return self.results
        except Error as e:
            print(f"Error while executing query: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        # No specific cleanup is required here as the DatabaseConnection handles connection cleanup
        pass

# Usage example
if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "database": "ALX_prodev",
        "user": "chris",
        "password": "D@tabreach2024"
    }

    query = "SELECT * FROM user_data WHERE age > %s"
    params = (25,)

    try:
        with DatabaseConnection(**db_config) as connection:
            with ExecuteQuery(connection, query, params) as results:
                # Print the results
                for row in results:
                    print(row)
    except Error as e:
        print(f"Database operation failed: {e}")
