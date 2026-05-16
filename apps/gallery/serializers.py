from rest_framework import serializers
from .models import GalleryMedia
from django.conf import settings
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


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
        
        def _url_exists(url: str) -> bool:
            if not url:
                return False
            try:
                req = Request(url, method='HEAD')
                with urlopen(req, timeout=10) as resp:
                    return getattr(resp, 'status', None) == 200
            except HTTPError as e:
                if e.code == 405:
                    try:
                        req2 = Request(url, method='GET')
                        with urlopen(req2, timeout=10) as resp2:
                            return getattr(resp2, 'status', None) == 200
                    except Exception:
                        return False
                return False
            except Exception:
                return False
        # Prefer the storage-provided URL when available
        if obj.media_file:
            try:
                file_url = obj.media_file.url
            except Exception:
                file_url = None

            # If storage returned an absolute URL, use it (optionally absolutize via request)
            if file_url and (file_url.startswith('http://') or file_url.startswith('https://')):
                # Supabase S3 URLs are often private (403). Convert to the public object URL shape and verify existence.
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
                                public = f"https://{project_host}/storage/v1/object/public/{bucket_from_url}/{object_key}"
                                if _url_exists(public):
                                    return public
                    except Exception:
                        pass

                # If the absolute file_url itself is publicly reachable, use it
                absolutized = request.build_absolute_uri(file_url) if request else file_url
                if _url_exists(absolutized):
                    return absolutized

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
                    if _url_exists(public_url):
                        return public_url
                except Exception:
                    pass

            # Fallback to building an absolute URL to the backend media path
            # Fallback to building an absolute URL to the backend media path, but verify it exists
            if file_url and request:
                abs_url = request.build_absolute_uri(file_url)
                if _url_exists(abs_url):
                    return abs_url
            # Last resort: return None if no reachable URL found
            return None
        return None
    
    def get_uploader(self, obj):
        """Return uploader info."""
        if obj.uploaded_by:
            return {
                'id': obj.uploaded_by.id,
                'name': obj.uploaded_by.get_full_name() or obj.uploaded_by.email,
            }
        return None
