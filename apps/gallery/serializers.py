from rest_framework import serializers
from .models import GalleryMedia


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
        if obj.media_file and request:
            return request.build_absolute_uri(obj.media_file.url)
        return obj.media_file.url if obj.media_file else None
    
    def get_uploader(self, obj):
        """Return uploader info."""
        if obj.uploaded_by:
            return {
                'id': obj.uploaded_by.id,
                'name': obj.uploaded_by.get_full_name() or obj.uploaded_by.email,
            }
        return None
