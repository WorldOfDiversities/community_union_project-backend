from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import OrganizationSettings
from .serializers import OrganizationSettingsSerializer


class OrganizationSettingsViewSet(viewsets.ViewSet):
    """
    API endpoint for organization settings.
    GET /api/v1/settings/ - Retrieve organization settings
    PUT /api/v1/settings/update/ - Update organization settings
    POST /api/v1/settings/upload-logo/ - Upload logo
    """
    
    permission_classes = [IsAuthenticated]
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    
    def list(self, request):
        """Get organization settings."""
        settings, _ = OrganizationSettings.objects.get_or_create(id=1)
        serializer = OrganizationSettingsSerializer(settings, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'], url_path='update')
    def update_settings(self, request):
        """Update organization settings."""
        # Check if user is admin
        if not request.user.is_staff:
            return Response(
                {'error': 'Only administrators can update settings.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        settings, _ = OrganizationSettings.objects.get_or_create(id=1)
        serializer = OrganizationSettingsSerializer(settings, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='upload-logo')
    def upload_logo(self, request):
        """Upload organization logo."""
        # Check if user is admin
        if not request.user.is_staff:
            return Response(
                {'error': 'Only administrators can upload logo.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        logo_file = request.FILES.get('logo')
        if not logo_file:
            return Response(
                {'error': 'No logo file provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        settings, _ = OrganizationSettings.objects.get_or_create(id=1)
        previous_logo = getattr(settings, 'logo', None)
        settings.logo = logo_file
        settings.save()

        try:
            if previous_logo and getattr(previous_logo, 'name', None) and previous_logo.name != settings.logo.name:
                previous_logo.storage.delete(previous_logo.name)
        except Exception:
            pass
        
        serializer = OrganizationSettingsSerializer(settings, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
