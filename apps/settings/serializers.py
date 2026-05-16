from rest_framework import serializers
from .models import OrganizationSettings
from apps.media_utils import resolve_media_url


class OrganizationSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    
    def get_logo_url(self, obj):
        if not obj.logo:
            return None

        request = self.context.get('request')
        try:
            logo_url = obj.logo.url
        except Exception:
            logo_url = None

        return resolve_media_url(
            raw_url=logo_url,
            storage_name=getattr(obj.logo, 'name', None),
            endpoint_url=None,
            bucket_name=None,
            storage=getattr(obj.logo, 'storage', None),
            request=request,
        )
    
    class Meta:
        model = OrganizationSettings
        fields = [
            'id',
            'union_name',
            'chapter_number',
            'primary_contact_email',
            'time_zone',
            'physical_address',
            'chapter_details',
            'logo',
            'logo_url',
            'dues_sms_enabled',
            'dues_email_enabled',
            'meeting_sms_enabled',
            'meeting_email_enabled',
            'member_updates_sms_enabled',
            'member_updates_email_enabled',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'logo_url']
