# Use a base image from Docker Hub
FROM python:3.10

# Set the working directory within the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install project dependencies
RUN pip install -r requirements.txt

# Specify the command to run when the container starts
CMD ["python", "app.py"]
