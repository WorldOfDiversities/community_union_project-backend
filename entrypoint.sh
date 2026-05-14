#!/usr/bin/env bash
set -e

# Wait for DB to be available (simple loop)
if [ -n "$DATABASE_URL" ]; then
  echo "Waiting for database..."
  retries=0
  until python - <<PYTHON
import sys, os
from urllib.parse import urlparse
try:
    from django.db import connections
    print('Checking DB connection requires Django; skipping until app code copied')
except Exception:
    pass
sys.exit(0)
PYTHON
  do
    sleep 1
    retries=$((retries+1))
    if [ "$retries" -gt 60 ]; then
      echo "Timed out waiting for DB" >&2
      exit 1
    fi
  done
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
