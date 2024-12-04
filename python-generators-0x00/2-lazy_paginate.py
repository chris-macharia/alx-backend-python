import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database with the given page size and offset.
    Args:
        page_size (int): Number of records per page.
        offset (int): Offset to fetch records from.
    Yields:
        list: A page of users from the user_data table.
    """
    connection = mysql.connector.connect(
        host="localhost",        # e.g., "localhost"
        user="chris",    # e.g., "root"
        password="D@tabreach2024",# Your MySQL password
        database="ALX_prodev" # The database containing the user_data table
    )
    cursor = connection.cursor(dictionary=True)

    try:
        # Execute the query with LIMIT and OFFSET for pagination
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        result = cursor.fetchall()
        yield result  # Yield the fetched page of users
    finally:
        cursor.close()
        connection.close()


def lazy_paginate(page_size):
    """
    Generator function that lazily loads pages of users from the database.
    Args:
        page_size (int): Number of records per page.
    Yields:
        list: A page of filtered users from the user_data table.
    """
    offset = 0  # Start with an offset of 0
    while True:
        # Fetch the next page of users
        page = paginate_users(page_size, offset)
        try:
            users = next(page)
            if not users:  # If no more users are returned, stop the generator
                break
            yield users  # Yield the page of users
            offset += page_size  # Increment the offset for the next page
        except StopIteration:
            break
