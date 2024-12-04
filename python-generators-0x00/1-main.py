#!/usr/bin/python3
from itertools import islice
stream_users_module = __import__('0-stream_users')  # Corrected for underscores

# Access the stream_users function from the imported module
stream_users = stream_users_module.stream_users

# Iterate over the generator function and print only the first 6 rows
for user in islice(stream_users(), 6):
    print(user)


