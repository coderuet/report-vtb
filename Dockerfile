# Use official Python runtime as a base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files
COPY main.py /app/

COPY code/ /app/code

COPY requirements.txt /app/

# Install dependencies (none in this case)
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the script
CMD ["python", "main.py"]