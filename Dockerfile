# Use official Python runtime as a base image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean \
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