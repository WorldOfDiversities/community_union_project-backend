from django.db import models

from apps.accounts.models import BaseModel, User


class Activity(BaseModel):
	STATUS_CHOICES = [
		("upcoming", "Upcoming"),
		("training", "Training"),
		("completed", "Completed"),
		("cancelled", "Cancelled"),
	]

	activity_id = models.CharField(max_length=20, unique=True)
	title = models.CharField(max_length=255)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES)
	scheduled_at = models.DateTimeField()
	location = models.CharField(max_length=255)
	organizer = models.CharField(max_length=255)
	attendees = models.PositiveIntegerField(default=0)

	class Meta:
		db_table = "activities_activity"
		ordering = ["scheduled_at", "-created_at"]
		verbose_name = "Activity"
		verbose_name_plural = "Activities"

	def __str__(self):
		return f"{self.activity_id} - {self.title}"


class ActivityAttendance(BaseModel):
	STATUS_CHOICES = [
		("Attended", "Attended"),
		("Missed", "Missed"),
	]

	member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activity_attendance")
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="attendance_records")
	status = models.CharField(max_length=20, choices=STATUS_CHOICES)
	attended_on = models.DateField(blank=True, null=True)

	class Meta:
		db_table = "activities_attendance"
		ordering = ["-attended_on", "-created_at"]
		verbose_name = "Activity Attendance"
		verbose_name_plural = "Activity Attendance"

	def __str__(self):
		return f"{self.member.email} - {self.activity.activity_id} - {self.status}"
