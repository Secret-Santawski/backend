# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image and set working directory as worskpace/backend
ENV APP_HOME /workspaces/backend
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Set the python path to the app directory
ENV PYTHONPATH "${PYTHONPATH}:/workspaces/backend"

# Get environment variables from environment
ARG ENVIRONMENT
ENV FIREBASE_CREDENTIALS_PATH="${FIREBASE_CREDENTIALS_PATH}"
ENV SENDER_EMAIL="${SENDER_EMAIL}"
ENV SENDER_PASSWORD="${SENDER_PASSWORD}"

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app