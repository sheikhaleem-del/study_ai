# Use official Python image
FROM python:3.10-slim

# Prevent Python buffering
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libgtk-3-0 \
    fonts-liberation \
    libjpeg62-turbo \
    libxshmfence1 \
    libglu1-mesa \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps

# Copy project files
COPY . .

# Expose Flask port
EXPOSE 5000

# Start app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "api:app"]
