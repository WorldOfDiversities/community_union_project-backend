from django.urls import path
from .views import MemberListView, MemberDetailView

app_name = "members"

urlpatterns = [
    path("", MemberListView.as_view(), name="list"),
    path("<int:id>/", MemberDetailView.as_view(), name="detail"),
]
