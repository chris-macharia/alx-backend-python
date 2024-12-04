#!/usr/bin/python3
import sys
processing = __import__('1-batch_processing')

try:
    # Iterate over the processed batches and print each batch
    for batch in processing.batch_processing(50):
        for user in batch:  # Iterate through the users in the filtered batch
            print(user)
except BrokenPipeError:
    sys.stderr.close()
