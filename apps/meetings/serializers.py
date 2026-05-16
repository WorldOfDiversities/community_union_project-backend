from rest_framework import serializers

from .models import Meeting
from apps.media_utils import resolve_media_url
from django.conf import settings


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
	image_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)

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

	def validate_image_url(self, value):
		if value in (None, ''):
			return ''

		resolved = resolve_media_url(
			raw_url=value,
			endpoint_url=getattr(settings, 'AWS_S3_ENDPOINT_URL', None),
			bucket_name=getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
		)
		if not resolved:
			raise serializers.ValidationError('Image URL must point to a reachable image or be empty.')
		return resolved

	def to_representation(self, instance):
		representation = super().to_representation(instance)
		representation['image_url'] = resolve_media_url(
			raw_url=getattr(instance, 'image_url', None),
			endpoint_url=getattr(settings, 'AWS_S3_ENDPOINT_URL', None),
			bucket_name=getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
		) or ''
		return representation
