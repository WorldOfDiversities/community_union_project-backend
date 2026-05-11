from django.contrib import admin

from .models import MemberAssignment, MemberCertification


@admin.register(MemberAssignment)
class MemberAssignmentAdmin(admin.ModelAdmin):
	list_display = ("title", "member", "is_active", "assigned_on", "created_at")
	list_filter = ("is_active", "assigned_on")
	search_fields = ("title", "member__email", "member__first_name", "member__last_name")


@admin.register(MemberCertification)
class MemberCertificationAdmin(admin.ModelAdmin):
	list_display = ("title", "member", "is_active", "issued_on", "expires_on", "created_at")
	list_filter = ("is_active", "issued_on", "expires_on")
	search_fields = ("title", "issued_by", "member__email", "member__first_name", "member__last_name")
