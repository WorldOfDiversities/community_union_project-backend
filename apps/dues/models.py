from django.db import models

from apps.accounts.models import BaseModel, User


class DuesPayment(BaseModel):
	STATUS_CHOICES = [
		("Current", "Current"),
		("Paid", "Paid"),
		("Overdue", "Overdue"),
	]

	member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dues_payments")
	billing_period = models.CharField(max_length=50)
	due_date = models.DateField()
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	method = models.CharField(max_length=100)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES)
	paid_on = models.DateField(blank=True, null=True)

	class Meta:
		db_table = "dues_payment"
		ordering = ["-due_date", "-created_at"]
		verbose_name = "Dues Payment"
		verbose_name_plural = "Dues Payments"

	def __str__(self):
		return f"{self.billing_period} - {self.member.email}"


class MemberStanding(BaseModel):
	member = models.OneToOneField(User, on_delete=models.CASCADE, related_name="standing")
	active_since_years = models.PositiveIntegerField(default=0)
	payment_rate = models.PositiveIntegerField(default=0)
	status_label = models.CharField(max_length=50)
	current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

	class Meta:
		db_table = "dues_member_standing"
		verbose_name = "Member Standing"
		verbose_name_plural = "Member Standings"

	def __str__(self):
		return f"{self.member.email} - {self.status_label}"
