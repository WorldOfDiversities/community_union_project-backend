from django.contrib import admin

from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
	list_display = ("meeting_id", "title", "category", "status", "scheduled_at", "location", "attendees")
	list_filter = ("category", "status")
	search_fields = ("meeting_id", "title", "location", "description")
