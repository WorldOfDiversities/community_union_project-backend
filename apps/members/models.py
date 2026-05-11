from django.db import models

from apps.accounts.models import BaseModel, User


class MemberAssignment(BaseModel):
	member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignments")
	title = models.CharField(max_length=150)
	description = models.TextField(blank=True, default="")
	assigned_on = models.DateField(blank=True, null=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		db_table = "members_assignment"
		ordering = ["-created_at"]
		verbose_name = "Member Assignment"
		verbose_name_plural = "Member Assignments"

	def __str__(self):
		return f"{self.title} - {self.member.email}"


class MemberCertification(BaseModel):
	member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certifications")
	title = models.CharField(max_length=150)
	issued_by = models.CharField(max_length=150, blank=True, default="")
	issued_on = models.DateField(blank=True, null=True)
	expires_on = models.DateField(blank=True, null=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		db_table = "members_certification"
		ordering = ["-issued_on", "-created_at"]
		verbose_name = "Member Certification"
		verbose_name_plural = "Member Certifications"

	def __str__(self):
		return f"{self.title} - {self.member.email}"
