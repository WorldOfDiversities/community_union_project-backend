"""
Django settings - Development environment overrides
"""

import os

from .base import *

# Override for development
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Development uses the same PostgreSQL DATABASE_URL path as production.

# Disable CORS restrictions in development
CORS_ALLOW_ALL_ORIGINS = True

# Email backend for development (console output)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Celery config for development (sync tasks)
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
