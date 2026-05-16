from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import GalleryMedia
from .serializers import GalleryMediaSerializer
from apps.media_utils import resolve_media_url
from django.conf import settings


class GalleryListCreateView(generics.ListCreateAPIView):
    """
    List all gallery media or upload new media.
    GET /api/v1/gallery/ - List all gallery media
    POST /api/v1/gallery/ - Upload new media
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GalleryMediaSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        """Return all gallery media, ordered by date taken (newest first)."""
        return GalleryMedia.objects.all().order_by('-date_taken', '-created_at')
    
    def list(self, request, *args, **kwargs):
        """Get paginated list of gallery media."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # Only return items that have a reachable media URL (avoid showing DB rows with missing storage objects)
        filtered = [item for item in serializer.data if item.get('media_url')]
        return Response(filtered)
    
    def create(self, request, *args, **kwargs):
        """Upload new media to gallery."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Automatically set the uploader to the current user
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryMediaDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = GalleryMedia.objects.all()
    lookup_field = 'id'

    def perform_destroy(self, instance):
        media_file = getattr(instance, 'media_file', None)
        storage = getattr(media_file, 'storage', None) if media_file else None
        name = getattr(media_file, 'name', None) if media_file else None
        if storage and name:
            try:
                storage.delete(name)
            except Exception:
                pass
        instance.delete()


class GalleryMediaDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific media item for download.
    GET /api/v1/gallery/{id}/ - Get media details
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GalleryMediaSerializer
    queryset = GalleryMedia.objects.all()
    lookup_field = 'id'
