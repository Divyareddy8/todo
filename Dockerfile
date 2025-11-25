FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Python dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose Flask port
EXPOSE 5000

# Run Flask app
CMD ["python3", "app.py"]