from django.db import models

from apps.accounts.models import BaseModel


class Meeting(BaseModel):
	CATEGORY_CHOICES = [
		("scheduled", "Scheduled"),
		("social_gathering", "Social Gathering"),
		("unlisted", "Unlisted"),
	]

	STATUS_CHOICES = [
		("upcoming", "Upcoming"),
		("completed", "Completed"),
		("cancelled", "Cancelled"),
	]

	meeting_id = models.CharField(max_length=20, unique=True)
	title = models.CharField(max_length=255)
	category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="scheduled")
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")
	scheduled_at = models.DateTimeField()
	location = models.CharField(max_length=255)
	attendees = models.PositiveIntegerField(default=0)
	action_items = models.PositiveIntegerField(default=0)
	description = models.TextField(blank=True)
	has_image = models.BooleanField(default=False)
	image_url = models.CharField(max_length=255, blank=True, default="")

	class Meta:
		db_table = "meetings_meeting"
		ordering = ["scheduled_at", "-created_at"]
		verbose_name = "Meeting"
		verbose_name_plural = "Meetings"

	def __str__(self):
		return f"{self.meeting_id} - {self.title}"
