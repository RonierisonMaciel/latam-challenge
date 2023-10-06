# syntax=docker/dockerfile:1.2
# Using the official Python latest image based on the Buster (Debian 10) release
FROM python:3.9-buster

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements files into the container at /app
COPY requirements.txt .
COPY requirements-dev.txt .
COPY requirements-test.txt .

# Copy the current directory contents into the container at /app
COPY . ./

# Install the Python dependencies from all the requirements files
RUN pip install -r requirements.txt -r requirements-dev.txt -r requirements-test.txt

# Inform Docker that the container listens on the specified port at runtime
EXPOSE 8080

# The command that will be executed when the container starts
# In this case, it starts the Uvicorn server for the application
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]

