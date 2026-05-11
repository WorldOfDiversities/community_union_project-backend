from rest_framework import serializers

from .models import Meeting


def format_date(value):
	if value is None:
		return None
	date_part = value.strftime("%B %d, %Y").replace(" 0", " ")
	return date_part


def format_time(value):
	if value is None:
		return None
	return value.strftime("%I:%M %p").lstrip("0")


class MeetingSerializer(serializers.ModelSerializer):
	date = serializers.SerializerMethodField()
	time = serializers.SerializerMethodField()
	category_label = serializers.SerializerMethodField()
	status_label = serializers.SerializerMethodField()

	class Meta:
		model = Meeting
		fields = [
			"meeting_id",
			"title",
			"category",
			"category_label",
			"status",
			"status_label",
			"date",
			"time",
			"location",
			"attendees",
			"action_items",
			"description",
			"has_image",
			"image_url",
			"scheduled_at",
		]

	def get_date(self, obj):
		return format_date(obj.scheduled_at)

	def get_time(self, obj):
		return format_time(obj.scheduled_at)

	def get_category_label(self, obj):
		return obj.get_category_display()

	def get_status_label(self, obj):
		return obj.get_status_display()
