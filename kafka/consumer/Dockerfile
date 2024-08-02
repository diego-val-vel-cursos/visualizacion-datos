# Use the official Python image as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the Python dependencies file to the container at /app
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# At the end, set the command to run when starting the container to Python interactive mode
# This is just to keep the container running. You'll execute Python scripts manually later.
CMD ["tail", "-f", "/dev/null"]
