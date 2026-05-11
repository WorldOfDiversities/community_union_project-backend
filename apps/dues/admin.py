from django.contrib import admin

from .models import DuesPayment, MemberStanding


@admin.register(DuesPayment)
class DuesPaymentAdmin(admin.ModelAdmin):
	list_display = ("billing_period", "member", "amount", "method", "status", "due_date", "paid_on")
	list_filter = ("status", "due_date")
	search_fields = ("billing_period", "member__email", "member__first_name", "member__last_name", "method")


@admin.register(MemberStanding)
class MemberStandingAdmin(admin.ModelAdmin):
	list_display = ("member", "status_label", "active_since_years", "payment_rate", "current_balance")
	search_fields = ("member__email", "member__first_name", "member__last_name", "status_label")
