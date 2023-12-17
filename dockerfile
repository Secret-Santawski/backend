# Use a base Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the source code into the container
COPY . .

# Install the project dependencies
RUN pip install -r requirements.txt

# Start the Flask application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 1 --timeout 0 src.app:app