# Use an official Python runtime as a parent image
FROM python:3.13-slim

ARG STORAGE_ACCOUNT_NAME
ENV STORAGE_ACCOUNT_NAME=$STORAGE_ACCOUNT_NAME
ARG STORAGE_ACCOUNT_KEY
ENV STORAGE_ACCOUNT_KEY=$STORAGE_ACCOUNT_KEY
ARG FILE_SHARE_NAME
ENV FILE_SHARE_NAME=$FILE_SHARE_NAME
ARG API_ID
ENV API_ID=$API_ID
ARG API_HASH
ENV API_HASH=$API_HASH
ARG CHAT_ID
ENV CHAT_ID=$CHAT_ID
ARG CHANNEL_ID
ENV CHANNEL_ID=$CHANNEL_ID

# Set the working directory in the container
WORKDIR /app

# Copy your Python script and entrypoint script to the container
COPY ./app.py /app/app.py
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y cifs-utils bash

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]