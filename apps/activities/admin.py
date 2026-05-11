from django.contrib import admin

from .models import Activity, ActivityAttendance


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
	list_display = ("activity_id", "title", "status", "scheduled_at", "location", "organizer", "attendees")
	list_filter = ("status", "scheduled_at")
	search_fields = ("activity_id", "title", "location", "organizer")


@admin.register(ActivityAttendance)
class ActivityAttendanceAdmin(admin.ModelAdmin):
	list_display = ("member", "activity", "status", "attended_on", "created_at")
	list_filter = ("status", "attended_on")
	search_fields = ("member__email", "member__first_name", "member__last_name", "activity__activity_id", "activity__title")
