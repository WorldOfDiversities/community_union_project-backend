from django.db.models import Sum
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Meeting
from .serializers import MeetingSerializer


class MeetingListView(generics.ListCreateAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = MeetingSerializer

	def get_queryset(self):
		return Meeting.objects.all().order_by("scheduled_at", "-created_at")

	def list(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		serializer = self.get_serializer(queryset, many=True)
		now = timezone.now()
		stats = {
			"total": queryset.count(),
			"upcoming": queryset.filter(status="upcoming").count(),
			"scheduled": queryset.filter(category="scheduled").count(),
			"socialGatherings": queryset.filter(category="social_gathering").count(),
			"actionItems": queryset.aggregate(total=Sum("action_items"))["total"] or 0,
			"thisMonth": queryset.filter(scheduled_at__year=now.year, scheduled_at__month=now.month).count(),
		}
		return Response({"results": serializer.data, "stats": stats})

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		return Response(serializer.data, status=201)


class MeetingDetailView(generics.RetrieveAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = MeetingSerializer
	lookup_field = "meeting_id"
	queryset = Meeting.objects.all()
