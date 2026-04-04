# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 8080

# Environment
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PORT=8080

# Seed DB and start server
ENTRYPOINT ["./entrypoint.sh"]
