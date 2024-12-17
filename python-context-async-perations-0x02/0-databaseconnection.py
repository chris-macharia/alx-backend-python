#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    """
    A custom context manager to handle opening and closing database connections automatically.
    """

    def __init__(self, host: str, database: str, user: str, password: str):
        """
        Initializes the DatabaseConnection with connection parameters.
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def __enter__(self):
        """
        Opens the database connection.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            if self.connection.is_connected():
                print("Connection established")
            return self.connection
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the database connection.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connection closed")


# Usage example
if __name__ == "__main__":
    # Replace with your database credentials
    db_config = {
        "host": "localhost",
        "database": "ALX_prodev",
        "user": "chris",
        "password": "D@tabreach2024",
    }

    query = "SELECT * FROM users"

    try:
        with DatabaseConnection(**db_config) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                print(row)
    except Error as e:
        print(f"Error occurred: {e}")
