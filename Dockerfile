# Dockerfile for reproducible builds on Render
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy dependency files first to leverage Docker cache
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

# Copy project
COPY . /app

# Collect static files and run migrations at container start via entrypoint
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
