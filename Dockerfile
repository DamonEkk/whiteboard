# Use an official Python slim image based on Debian (close to Ubuntu)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code
COPY . .

# Expose port your Flask app will use
EXPOSE 5000

# Run your app (adjust entry.py if needed)
CMD ["python", "entry.py"]
