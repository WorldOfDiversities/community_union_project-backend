from django.contrib import admin
from .models import GalleryMedia


@admin.register(GalleryMedia)
class GalleryMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'media_type', 'date_taken', 'uploaded_by', 'created_at')
    list_filter = ('media_type', 'date_taken', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
