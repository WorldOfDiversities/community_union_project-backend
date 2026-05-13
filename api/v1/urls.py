from django.urls import path, include

urlpatterns = [
    path("auth/", include("apps.accounts.urls")),
    path("communications/", include("apps.notifications.urls")),
    path("members/", include("apps.members.urls")),
    path("activities/", include("apps.activities.urls")),
    path("meetings/", include("apps.meetings.urls")),
    path("dues/", include("apps.dues.urls")),
    path("settings/", include("apps.settings.urls")),
    path("gallery/", include("apps.gallery.urls")),
    # etc.
]

