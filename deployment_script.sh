# File location: deployment_script.sh

#!/bin/bash

# A simple script to build and deploy the Vidya application using Docker Compose.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Starting Vidya Deployment Process ---"

# Step 1: Build the Docker image
echo "Building the Docker image..."
docker-compose build --no-cache

# Check if the build was successful
if [ $? -ne 0 ]; then
    echo "Docker build failed. Exiting."
    exit 1
fi

echo "Docker image built successfully."

# Step 2: Start the containers
echo "Starting the Vidya application containers..."
# -d runs the containers in detached mode (in the background)
docker-compose up -d

# Check if the containers started successfully
if [ $? -ne 0 ]; then
    echo "Docker Compose failed to start containers. Exiting."
    exit 1
fi

echo "Deployment successful! The application is running."
echo "You can check the logs with: docker-compose logs -f"
echo "To stop the application, run: docker-compose down"
echo "--- Deployment Finished ---"
