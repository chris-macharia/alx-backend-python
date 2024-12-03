import mysql.connector
import csv
import uuid
from decimal import Decimal

# Function to connect to MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change to your MySQL host
            user='chris',  # Replace with your MySQL username
            password='D@tabreach2024'  # Replace with your MySQL password
        )
        connection_timeout=300
        print("Database connection established successfully.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create the ALX_prodev database if it does not exist
def create_database(connection):
    try:
        if not connection.is_connected():
            print("Connection lost, attempting to reconnect...")
            connection.close()
            connection = mysql.connector.connect(
                host="localhost",
                user="chris",  # Replace with your MySQL username
                password="D@tabreach2024"  # Replace with your MySQL password
            )
            print("Reconnected to MySQL.")
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
        print("Database created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.close()

# Function to connect to the ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change to your MySQL host
            user='chris',  # Replace with your MySQL username
            password='D@tabreach2024',  # Replace with your MySQL password
            database='ALX_prodev'
        )
        print("Connected to the ALX_prodev database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create the user_data table if it does not exist
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(10,2) NOT NULL
    );
    """)
    print("Table user_data created (if it didn't exist).")
    cursor.close()

# Function to insert data into the user_data table
def insert_data(connection, data):
    cursor = connection.cursor()
    for row in data:
        user_id = str(uuid.uuid4())  # Generate a new UUID for each user
        name = row['name']
        email = row['email']
        age = Decimal(row['age'])
        cursor.execute("""
        INSERT INTO user_data (user_id, name, email, age)
        SELECT %s, %s, %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM user_data WHERE email = %s);
        """, (user_id, name, email, age, email))
    connection.commit()
    print(f"{len(data)} rows inserted into user_data table.")
    cursor.close()

# Function to read data from the CSV file
def read_csv(file_path):
    data = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

# Generator function to stream rows one by one from the database
def stream_rows(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    for row in cursor:
        yield row
    cursor.close()

# Main function to run the script
def main():
    # Connect to MySQL server
    connection = connect_db()
    if not connection:
        return

    # Create the database if it does not exist
    create_database(connection)

    # Connect to the ALX_prodev database
    connection = connect_to_prodev()
    if not connection:
        return

    # Create the table if it does not exist
    create_table(connection)

    # Read data from the CSV file
    file_path = 'data.csv'  # Provide the correct path to your CSV file
    data = read_csv(file_path)

    # Insert data into the table
    insert_data(connection, data)

    # Stream rows one by one from the user_data table
    print("Streaming rows from the user_data table:")
    for row in stream_rows(connection):
        print(row)

    # Close the connection
    connection.close()

if __name__ == "__main__":
    main()
