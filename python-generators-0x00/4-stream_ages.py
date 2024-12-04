import mysql.connector

def stream_user_ages():
    """
    Generator function to yield user ages one by one from the database.
    Yields:
        int: User's age from the user_data table.
    """
    connection = mysql.connector.connect(
        host="localhost",        # e.g., "localhost"
        user="chris",    # e.g., "root"
        password="D@tabreach2024",# Your MySQL password
        database="ALX_prodev" # The database containing the user_data table
    )
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT age FROM user_data")  # Fetch only the age column
        for row in cursor:
            yield row[0]  # Yield the age
    finally:
        cursor.close()
        connection.close()


def calculate_average_age():
    """
    Function to calculate the average age of users using the generator.
    Uses a single pass over the data to calculate the sum and count of ages.
    """
    total_age = 0
    user_count = 0

    # Iterate over the ages yielded by the generator
    for age in stream_user_ages():
        total_age += age
        user_count += 1

    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age}")
    else:
        print("No users found.")


# Run the average age calculation
if __name__ == "__main__":
    calculate_average_age()
