"""
Django settings - Base configuration shared across all environments.

CUMS Backend - Community Union Management System
"""

import os
from pathlib import Path
from datetime import timedelta

from django.core.exceptions import ImproperlyConfigured

# Optional helper to parse DATABASE_URL
import dj_database_url

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / "apps"

# Core Settings
# Support both `SECRET_KEY` and `DJANGO_SECRET_KEY` environment variable names
SECRET_KEY = os.environ.get("SECRET_KEY") or os.environ.get("DJANGO_SECRET_KEY") or "django-insecure-dev-key-change-in-production"
DEBUG = os.environ.get("DEBUG", "False") == "True"
# Normalize ALLOWED_HOSTS from comma-separated env var; allow blank -> []
_allowed = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(",") if h.strip()]

# If running on Render, it may expose the external hostname in env vars.
# Accept common Render env vars and add them to ALLOWED_HOSTS automatically.
_render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME") or os.environ.get("RENDER_EXTERNAL_URL")
if _render_host:
    try:
        # if a full URL was provided, extract the host portion
        from urllib.parse import urlparse

        parsed = urlparse(_render_host)
        host = parsed.netloc or parsed.path
    except Exception:
        host = _render_host

    host = host.strip()
    if host and host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)

# Treat media as persistent storage when object storage credentials are provided.
USE_OBJECT_STORAGE = bool(
    os.environ.get("AWS_ACCESS_KEY_ID")
    and os.environ.get("AWS_SECRET_ACCESS_KEY")
    and os.environ.get("AWS_STORAGE_BUCKET_NAME")
)

if USE_OBJECT_STORAGE:
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "us-east-1")
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# Print ALLOWED_HOSTS at startup to help debug deploy issues
print("ALLOWED_HOSTS=", ALLOWED_HOSTS)

# Application definition
INSTALLED_APPS = [
    # Django defaults
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",

    # Project apps
    "apps.accounts",
    "apps.members",
    "apps.activities",
    "apps.meetings",
    "apps.dues",
    "apps.notifications",
    "apps.reports",
    "apps.settings",
    "apps.gallery",
]

if USE_OBJECT_STORAGE:
    # Guard appending to INSTALLED_APPS in case settings are being
    # imported in an unexpected order (some deploy environments may
    # load partial modules). This avoids raising NameError during import.
    if "INSTALLED_APPS" in globals():
        INSTALLED_APPS.append("storages")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise ImproperlyConfigured("DATABASE_URL is required and must point to Supabase.")

DATABASES = {
    "default": dj_database_url.parse(database_url, conn_max_age=600, ssl_require=True)
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = []

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "accounts.User"

# REST Framework Configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# Simple JWT Configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": os.environ.get("SECRET_KEY", "django-insecure-dev-key-change-in-production"),
    "VERIFYING_KEY": None,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3002,http://127.0.0.1:3002,https://community-union-project.vercel.app"
).split(",")

CORS_ALLOW_CREDENTIALS = True

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
