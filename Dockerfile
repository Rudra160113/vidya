# File location: Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000 8765

# Define environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "vidya/main.py"]
