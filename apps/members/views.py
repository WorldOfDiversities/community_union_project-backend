from rest_framework import generics, permissions

from apps.accounts.models import User

from .serializers import MemberDetailSerializer, MemberSerializer


class MemberListView(generics.ListAPIView):
	"""List active members for dashboard consumption.

	Returns active users ordered by newest first. Uses pagination if configured
	in the project settings (DRF pagination).
	"""
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = MemberSerializer

	def get_queryset(self):
		return User.objects.filter(is_active=True).order_by("-created_at")


class MemberDetailView(generics.RetrieveAPIView):
	"""Retrieve a single member's details.

	Returns full member information including profile, contact, and status details.
	"""
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = MemberDetailSerializer
	queryset = User.objects.all().select_related("standing").prefetch_related(
		"dues_payments",
		"assignments",
		"certifications",
		"activity_attendance__activity",
	)
	lookup_field = 'id'
