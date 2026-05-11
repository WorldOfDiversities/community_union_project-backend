from django.contrib import admin
from .models import OrganizationSettings


@admin.register(OrganizationSettings)
class OrganizationSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General Settings', {
            'fields': ('union_name', 'chapter_number', 'primary_contact_email', 'time_zone')
        }),
        ('Union Info', {
            'fields': ('physical_address', 'chapter_details', 'logo_url')
        }),
        ('Notification Preferences', {
            'fields': (
                'dues_sms_enabled',
                'dues_email_enabled',
                'meeting_sms_enabled',
                'meeting_email_enabled',
                'member_updates_sms_enabled',
                'member_updates_email_enabled',
            )
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # Only allow one settings record
        return OrganizationSettings.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False
