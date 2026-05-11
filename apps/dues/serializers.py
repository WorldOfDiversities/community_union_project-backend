from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import DuesPayment, MemberStanding

User = get_user_model()


def format_money(value):
	return f"${value:.2f}"


def format_date(value):
	return value.strftime("%B %d, %Y").replace(" 0", " ") if value else None


class DuesPaymentSerializer(serializers.ModelSerializer):
	member_email = serializers.EmailField(write_only=True)
	member_name = serializers.SerializerMethodField()
	member_id = serializers.SerializerMethodField()
	dueDate = serializers.SerializerMethodField()
	amountDisplay = serializers.SerializerMethodField()

	class Meta:
		model = DuesPayment
		fields = [
			"id",
			"member_email",
			"member_name",
			"member_id",
			"billing_period",
			"due_date",
			"dueDate",
			"amount",
			"amountDisplay",
			"method",
			"status",
			"paid_on",
		]
		extra_kwargs = {
			"id": {"read_only": True},
			"due_date": {"required": True},
			"amount": {"required": True},
			"method": {"required": True},
			"status": {"required": True},
			"billing_period": {"required": True},
		}

	def get_dueDate(self, obj):
		return format_date(obj.due_date)

	def get_amountDisplay(self, obj):
		return format_money(obj.amount)

	def get_member_name(self, obj):
		full_name = obj.member.get_full_name().strip()
		return full_name or obj.member.email

	def get_member_id(self, obj):
		return obj.member.id

	def create(self, validated_data):
		member_email = validated_data.pop("member_email")
		member = User.objects.get(email=member_email)
		validated_data["member"] = member
		return super().create(validated_data)


class MemberStandingSerializer(serializers.ModelSerializer):
	current_balance = serializers.SerializerMethodField()

	class Meta:
		model = MemberStanding
		fields = ["active_since_years", "payment_rate", "status_label", "current_balance"]

	def get_current_balance(self, obj):
		return format_money(obj.current_balance)
