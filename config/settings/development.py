"""
Django settings - Development environment overrides
"""

from .base import *

# Override for development
DEBUG = True
ALLOWED_HOSTS = ["*"]

# SQLite for local development (or PostgreSQL if preferred)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Disable CORS restrictions in development
CORS_ALLOW_ALL_ORIGINS = True

# Email backend for development (console output)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Celery config for development (sync tasks)
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
