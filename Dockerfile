# Use official Python runtime as a base image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    pkg-config \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY main.py /app/

COPY code/ /app/code

COPY requirements.txt /app/

# Install dependencies (none in this case)
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080

# Command to run the script
CMD ["python", "main.py"]