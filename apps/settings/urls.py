from django.urls import path
from .views import OrganizationSettingsViewSet

urlpatterns = [
    path('', OrganizationSettingsViewSet.as_view({'get': 'list'}), name='settings-list'),
    path('update/', OrganizationSettingsViewSet.as_view({'put': 'update_settings'}), name='settings-update'),
    path('upload-logo/', OrganizationSettingsViewSet.as_view({'post': 'upload_logo'}), name='settings-upload-logo'),
]
