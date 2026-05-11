from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Announcement
from .serializers import AnnouncementSerializer


class BroadcastView(APIView):
    """Create a new announcement/broadcast."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            announcement = Announcement.objects.create(
                subject=serializer.validated_data['subject'],
                body=serializer.validated_data['body'],
                sender=request.user if request.user.is_authenticated else None,
            )
            out = AnnouncementSerializer(announcement).data
            return Response(out, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BroadcastListView(APIView):
    """List recent announcements."""
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Announcement.objects.all()
        serializer = AnnouncementSerializer(qs, many=True)
        return Response(serializer.data)
from rest_framework import viewsets


# TODO: Create Notification viewsets here
