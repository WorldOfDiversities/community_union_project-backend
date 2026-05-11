from django.urls import path

from .views import ActivityDetailView, ActivityListView

app_name = "activities"

urlpatterns = [
    path("", ActivityListView.as_view(), name="list"),
    path("<str:activity_id>/", ActivityDetailView.as_view(), name="detail"),
]
