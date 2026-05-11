from django.db.models import Sum
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import DuesPayment, MemberStanding
from .serializers import DuesPaymentSerializer, MemberStandingSerializer


class DuesPaymentListView(generics.ListCreateAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = DuesPaymentSerializer

	def get_queryset(self):
		return DuesPayment.objects.select_related("member").all().order_by("-due_date", "-created_at")

	def list(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		serializer = self.get_serializer(queryset, many=True)
		stats = {
			"totalCollected": queryset.filter(status="Paid").aggregate(total=Sum("amount"))["total"] or 0,
			"totalOutstanding": queryset.filter(status="Current").aggregate(total=Sum("amount"))["total"] or 0,
			"totalOverdue": queryset.filter(status="Overdue").aggregate(total=Sum("amount"))["total"] or 0,
			"records": queryset.count(),
		}
		return Response({"results": serializer.data, "stats": stats})


class MemberStandingListView(generics.ListAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = MemberStandingSerializer
	queryset = MemberStanding.objects.select_related("member").all().order_by("-payment_rate", "-current_balance")
