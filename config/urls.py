"""
Root URL configuration for CUMS API
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    """Health check endpoint."""
    return JsonResponse({
        "status": "ok",
        "message": "Community Union Management System API v1.0.0",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/v1/",
        }
    })


urlpatterns = [
    # Health check
    path("", health_check, name="health_check"),

    # Admin
    path("admin/", admin.site.urls),

    # API v1
    path("api/v1/", include("api.v1.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
