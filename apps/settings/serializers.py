from rest_framework import serializers
from .models import OrganizationSettings


class OrganizationSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    
    def get_logo_url(self, obj):
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None
    
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
