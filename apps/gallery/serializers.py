from rest_framework import serializers
from .models import GalleryMedia
from django.conf import settings
from apps.media_utils import resolve_media_url


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
        endpoint = getattr(settings, 'AWS_S3_ENDPOINT_URL', None)
        bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)

        if not obj.media_file:
            return None

        try:
            file_url = obj.media_file.url
        except Exception:
            file_url = None

        return resolve_media_url(
            raw_url=file_url,
            storage_name=getattr(obj.media_file, 'name', None),
            endpoint_url=endpoint,
            bucket_name=bucket,
            storage=getattr(obj.media_file, 'storage', None),
            request=request,
        )
    
    def get_uploader(self, obj):
        """Return uploader info."""
        if obj.uploaded_by:
            return {
                'id': obj.uploaded_by.id,
                'name': obj.uploaded_by.get_full_name() or obj.uploaded_by.email,
            }
        return None
