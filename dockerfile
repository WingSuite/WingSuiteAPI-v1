# Use a specific version of the Python image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app/WingSuiteAPI

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies, including gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Set the environment variable RUN_MODE
ENV RUN_MODE 1

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]