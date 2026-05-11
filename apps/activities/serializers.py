from rest_framework import serializers

from .models import Activity, ActivityAttendance


def format_date_time(value):
	if value is None:
		return None
	date_part = value.strftime("%B %d, %Y").replace(" 0", " ")
	time_part = value.strftime("%I:%M %p").lstrip("0")
	return f"{date_part} • {time_part}"


class ActivitySerializer(serializers.ModelSerializer):
	date = serializers.SerializerMethodField()

	class Meta:
		model = Activity
		fields = ["activity_id", "title", "status", "date", "location", "organizer", "attendees", "scheduled_at"]

	def get_date(self, obj):
		return format_date_time(obj.scheduled_at)


class ActivityAttendanceSerializer(serializers.ModelSerializer):
	activity_id = serializers.CharField(source="activity.activity_id")
	title = serializers.CharField(source="activity.title")
	date = serializers.SerializerMethodField()

	class Meta:
		model = ActivityAttendance
		fields = ["activity_id", "title", "date", "status"]

	def get_date(self, obj):
		return obj.attended_on.strftime("%Y-%m-%d") if obj.attended_on else None
