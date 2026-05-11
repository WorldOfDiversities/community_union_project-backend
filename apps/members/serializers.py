from rest_framework import serializers

from apps.accounts.models import User
from apps.activities.models import ActivityAttendance
from apps.dues.models import DuesPayment, MemberStanding
from .models import MemberAssignment, MemberCertification


def format_money(value):
    return f"${value:.2f}"


def format_date(value, pattern="%B %d, %Y"):
    if value is None:
        return None
    return value.strftime(pattern).replace(" 0", " ")


def format_datetime(value):
    if value is None:
        return None
    date_part = value.strftime("%B %d, %Y").replace(" 0", " ")
    time_part = value.strftime("%I:%M %p").lstrip("0")
    return f"{date_part} • {time_part}"


class MemberSerializer(serializers.ModelSerializer):
	"""Serializer for exposing member information to the frontend."""
	full_name = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = [
			"id",
			"email",
			"full_name",
			"role",
			"phone",
			"is_active",
			"created_at",
			"avatar_url",
			"last_login",
		]
		read_only_fields = ["id", "created_at", "last_login"]

	def get_full_name(self, obj):
		return obj.get_full_name() or obj.email


class DuesPaymentSerializer(serializers.ModelSerializer):
	period = serializers.CharField(source="billing_period")
	dueDate = serializers.SerializerMethodField()
	amount = serializers.SerializerMethodField()

	class Meta:
		model = DuesPayment
		fields = ["period", "dueDate", "amount", "method", "status"]

	def get_dueDate(self, obj):
		return format_date(obj.due_date)

	def get_amount(self, obj):
		return format_money(obj.amount)


class MemberStandingSerializer(serializers.ModelSerializer):
	current_balance = serializers.SerializerMethodField()

	class Meta:
		model = MemberStanding
		fields = ["active_since_years", "payment_rate", "status_label", "current_balance"]

	def get_current_balance(self, obj):
		return format_money(obj.current_balance)


class MemberAssignmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = MemberAssignment
		fields = ["title", "description", "assigned_on", "is_active"]


class MemberCertificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = MemberCertification
		fields = ["title", "issued_by", "issued_on", "expires_on", "is_active"]


class ActivityAttendanceSerializer(serializers.ModelSerializer):
	activity_id = serializers.CharField(source="activity.activity_id")
	title = serializers.CharField(source="activity.title")
	date = serializers.SerializerMethodField()

	class Meta:
		model = ActivityAttendance
		fields = ["activity_id", "title", "date", "status"]

	def get_date(self, obj):
		return format_date(obj.attended_on or obj.activity.scheduled_at.date(), "%Y-%m-%d")


class MemberDetailSerializer(MemberSerializer):
	dues_history = serializers.SerializerMethodField()
	standing = serializers.SerializerMethodField()
	assignments = serializers.SerializerMethodField()
	certifications = serializers.SerializerMethodField()
	activity_attendance = serializers.SerializerMethodField()

	class Meta(MemberSerializer.Meta):
		fields = MemberSerializer.Meta.fields + [
			"dues_history",
			"standing",
			"assignments",
			"certifications",
			"activity_attendance",
		]

	def get_dues_history(self, obj):
		payments = obj.dues_payments.all().order_by("-due_date")
		return DuesPaymentSerializer(payments, many=True).data

	def get_standing(self, obj):
		standing = getattr(obj, "standing", None)
		return MemberStandingSerializer(standing).data if standing else None

	def get_assignments(self, obj):
		assignments = obj.assignments.filter(is_active=True).order_by("-created_at")
		return [assignment.title for assignment in assignments]

	def get_certifications(self, obj):
		certifications = obj.certifications.filter(is_active=True).order_by("-issued_on", "-created_at")
		return MemberCertificationSerializer(certifications, many=True).data

	def get_activity_attendance(self, obj):
		records = obj.activity_attendance.select_related("activity").all().order_by("-attended_on", "-created_at")
		return ActivityAttendanceSerializer(records, many=True).data
