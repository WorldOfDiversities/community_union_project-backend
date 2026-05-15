#!/usr/bin/env bash
set -e

if [ -n "$DATABASE_URL" ]; then
  echo "Checking database connection..."
  python - <<'PYTHON'
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from django.db import connection

connection.ensure_connection()
print("Database connection OK")
PYTHON
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
