# Use Python base image for AMD64
FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY process_pdfs.py .

# Default command to process PDFs
CMD ["python", "process_pdfs.py"]