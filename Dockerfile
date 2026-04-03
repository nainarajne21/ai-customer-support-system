# Dockerfile - Packages your project for Hugging Face
FROM python:3.10-slim

WORKDIR /app

# Copy all files
COPY requirements.txt .
COPY *.py .
COPY openenv.yaml .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your inference
CMD ["python", "inference.py"]