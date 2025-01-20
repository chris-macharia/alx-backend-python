# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /messaging_app

# Copy the current directory contents into the container at /messaging_app
COPY . /messaging_app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside the container
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver", "192.168.33.10:8000"]
