from django.urls import path

from .views import DuesPaymentListView, MemberStandingListView

app_name = "dues"

urlpatterns = [
    path("payments/", DuesPaymentListView.as_view(), name="payments"),
    path("standing/", MemberStandingListView.as_view(), name="standing"),
]
