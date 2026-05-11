from rest_framework import serializers
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ['id', 'subject', 'body', 'sender', 'created_at']

    def get_sender(self, obj):
        if obj.sender:
            return f"{obj.sender.first_name} {obj.sender.last_name}".strip() or obj.sender.email
        return None
from rest_framework import serializers


# TODO: Create Notification serializers here
