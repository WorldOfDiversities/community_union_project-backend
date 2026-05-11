from django.urls import path
from .views import BroadcastView, BroadcastListView

app_name = "notifications"

urlpatterns = [
    path('broadcast/', BroadcastView.as_view(), name='broadcast'),
    path('broadcasts/', BroadcastListView.as_view(), name='broadcasts'),
]
