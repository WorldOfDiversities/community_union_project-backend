from rest_framework import serializers
from .models import GalleryMedia
from django.conf import settings
from urllib.parse import urlparse


class GalleryMediaSerializer(serializers.ModelSerializer):
    """Serializer for gallery media items."""
    media_url = serializers.SerializerMethodField()
    uploader = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryMedia
        fields = [
            'id',
            'title',
            'description',
            'media_file',
            'media_url',
            'media_type',
            'date_taken',
            'uploader',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'media_url', 'uploader']
    
    def get_media_url(self, obj):
        """Build absolute URL for media file."""
        request = self.context.get('request')
        # Prefer the storage-provided URL when available
        if obj.media_file:
            try:
                file_url = obj.media_file.url
            except Exception:
                file_url = None

            # If storage returned an absolute URL, use it (optionally absolutize via request)
            if file_url and (file_url.startswith('http://') or file_url.startswith('https://')):
                # Supabase S3 URLs are often private (403). Convert to the public object URL shape.
                if '.storage.supabase.co' in file_url and '/storage/v1/s3/' in file_url:
                    try:
                        parsed = urlparse(file_url)
                        project_host = parsed.netloc.replace('.storage.supabase.co', '.supabase.co')
                        # Keep the object key after /storage/v1/s3/<bucket>/
                        path = parsed.path
                        marker = '/storage/v1/s3/'
                        idx = path.find(marker)
                        if idx >= 0:
                            remainder = path[idx + len(marker):].lstrip('/')
                            parts = remainder.split('/', 1)
                            if len(parts) == 2:
                                bucket_from_url, object_key = parts
                                return f"https://{project_host}/storage/v1/object/public/{bucket_from_url}/{object_key}"
                    except Exception:
                        pass
                return request.build_absolute_uri(file_url) if request else file_url

            # If we have a Supabase/S3 endpoint configured, construct the public object URL
            endpoint = getattr(settings, 'AWS_S3_ENDPOINT_URL', None)
            bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
            name = getattr(obj.media_file, 'name', None)
            if endpoint and bucket and name:
                try:
                    parsed = urlparse(endpoint)
                    host = parsed.netloc
                    # Convert storage host ("<ref>.storage.supabase.co") to public host ("<ref>.supabase.co")
                    project_host = host.replace('.storage.supabase.co', '.supabase.co')
                    public_url = f"https://{project_host}/storage/v1/object/public/{bucket}/{name}"
                    return public_url
                except Exception:
                    pass

            # Fallback to building an absolute URL to the backend media path
            if file_url and request:
                return request.build_absolute_uri(file_url)
            return file_url or name or None
        return None
    
    def get_uploader(self, obj):
        """Return uploader info."""
        if obj.uploaded_by:
            return {
                'id': obj.uploaded_by.id,
                'name': obj.uploaded_by.get_full_name() or obj.uploaded_by.email,
            }
        return None
