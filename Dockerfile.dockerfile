FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create models directory
RUN mkdir -p /app/models

# Copy application code
COPY app.py .

# The model will be downloaded during the build process
# (We'll handle this in buildspec.yml)

# Expose port (if you add a web server later)
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]