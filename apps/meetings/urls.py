from django.urls import path

from .views import MeetingDetailView, MeetingListView

app_name = "meetings"

urlpatterns = [
    path("", MeetingListView.as_view(), name="list"),
    path("<str:meeting_id>/", MeetingDetailView.as_view(), name="detail"),
]
