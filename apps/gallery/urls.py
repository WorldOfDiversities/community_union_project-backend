from django.urls import path
from .views import GalleryListCreateView, GalleryMediaDetailView, GalleryMediaDeleteView

app_name = "gallery"

urlpatterns = [
    path("", GalleryListCreateView.as_view(), name="list-create"),
    path("<int:id>/", GalleryMediaDetailView.as_view(), name="detail"),
    path("<int:id>/delete/", GalleryMediaDeleteView.as_view(), name="delete"),
]
