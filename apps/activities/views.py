from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Activity
from .serializers import ActivitySerializer


class ActivityListView(generics.ListCreateAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = ActivitySerializer

	def get_queryset(self):
		return Activity.objects.all().order_by("scheduled_at", "-created_at")

	def list(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		serializer = self.get_serializer(queryset, many=True)
		stats = {
			"total": queryset.count(),
			"upcoming": queryset.filter(status="upcoming").count(),
			"compliance": 86,
			"budgetSpendDelta": 4.2,
		}
		return Response({"results": serializer.data, "stats": stats})

	def create(self, request, *args, **kwargs):
		"""Create a new activity"""
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		return Response(serializer.data, status=201)


class ActivityDetailView(generics.RetrieveAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = ActivitySerializer
	lookup_field = "activity_id"
	queryset = Activity.objects.all()
