# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Flask
RUN pip install --no-cache-dir flask

# Copy source files
COPY . .

# Expose port
EXPOSE 5000

# Run Flask server
CMD ["python", "-m", "src.server"]
