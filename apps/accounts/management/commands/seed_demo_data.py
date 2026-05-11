from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.activities.models import Activity, ActivityAttendance
from apps.dues.models import DuesPayment, MemberStanding
from apps.members.models import MemberAssignment, MemberCertification
from apps.meetings.models import Meeting

User = get_user_model()

DEMO_USERS = [
    {
        "email": "abdulazizkarim1073@gmail.com",
        "full_name": "Aziz Karim",
        "role": "member",
        "phone": "+1-555-0101",
        "avatar_url": "/image.jpg",
        "password": "Password123!",
    },
    {
        "email": "test1778200286@example.com",
        "full_name": "Test User",
        "role": "member",
        "phone": "+1-555-0102",
        "avatar_url": "/image1.jpg",
        "password": "Password123!",
    },
    {
        "email": "ruth.miles@example.org",
        "full_name": "Ruth Miles",
        "role": "secretary",
        "phone": "+1-555-0103",
        "avatar_url": "/image2.jpg",
        "password": "Password123!",
    },
    {
        "email": "maya.choi@example.org",
        "full_name": "Maya Choi",
        "role": "member",
        "phone": "+1-555-0104",
        "avatar_url": "/image3.jpg",
        "password": "Password123!",
    },
    {
        "email": "samuel.lee@example.org",
        "full_name": "Samuel Lee",
        "role": "member",
        "phone": "+1-555-0105",
        "avatar_url": "/image5.jpg",
        "password": "Password123!",
    },
    {
        "email": "linda.green@example.org",
        "full_name": "Linda Green",
        "role": "member",
        "phone": "+1-555-0106",
        "avatar_url": "/image6.jpg",
        "password": "Password123!",
    },
    {
        "email": "james.howard@example.org",
        "full_name": "James Howard",
        "role": "member",
        "phone": "+1-555-0107",
        "avatar_url": "/image7.jpg",
        "password": "Password123!",
    },
    {
        "email": "alex.brown@example.org",
        "full_name": "Alex Brown",
        "role": "member",
        "phone": "+1-555-0108",
        "avatar_url": "/image8.jpg",
        "password": "Password123!",
    },
    {
        "email": "mariam.noor@example.org",
        "full_name": "Mariam Noor",
        "role": "member",
        "phone": "+1-555-0109",
        "avatar_url": "/image9.jpg",
        "password": "Password123!",
    },
    {
        "email": "c.ruiz@example.org",
        "full_name": "Carlos Ruiz",
        "role": "member",
        "phone": "+1-555-0110",
        "avatar_url": "/image10.jpg",
        "password": "Password123!",
    },
]

DEMO_ACTIVITIES = [
    {
        "activity_id": "ACT-001",
        "title": "Quarterly Strategy Session",
        "status": "upcoming",
        "scheduled_at": "2024-12-15T10:00:00",
        "location": "Main Conference Room",
        "organizer": "Board of Directors",
        "attendees": 24,
    },
    {
        "activity_id": "ACT-002",
        "title": "Safety Protocols Workshop",
        "status": "training",
        "scheduled_at": "2024-12-20T14:00:00",
        "location": "Training Hall A",
        "organizer": "Safety Committee",
        "attendees": 45,
    },
    {
        "activity_id": "ACT-003",
        "title": "Annual Unity Gala 2023",
        "status": "completed",
        "scheduled_at": "2023-12-08T18:00:00",
        "location": "Grand Ballroom Hotel",
        "organizer": "Social Committee",
        "attendees": 156,
    },
    {
        "activity_id": "ACT-004",
        "title": "Grievance Committee Review",
        "status": "upcoming",
        "scheduled_at": "2024-12-27T15:00:00",
        "location": "Virtual - Zoom Link",
        "organizer": "HR Department",
        "attendees": 8,
    },
    {
        "activity_id": "ACT-005",
        "title": "First Aid Certification",
        "status": "cancelled",
        "scheduled_at": "2024-12-18T09:00:00",
        "location": "Medical Training Unit",
        "organizer": "Health & Wellness",
        "attendees": 32,
    },
    {
        "activity_id": "ACT-006",
        "title": "Budgetary Planning Committee",
        "status": "completed",
        "scheduled_at": "2024-11-30T13:00:00",
        "location": "Conference Room B",
        "organizer": "Finance Team",
        "attendees": 14,
    },
    {
        "activity_id": "ACT-007",
        "title": "Member Onboarding Session",
        "status": "training",
        "scheduled_at": "2025-01-10T11:00:00",
        "location": "Hall C",
        "organizer": "Membership Office",
        "attendees": 18,
    },
    {
        "activity_id": "ACT-008",
        "title": "Community Outreach Drive",
        "status": "upcoming",
        "scheduled_at": "2025-01-18T08:30:00",
        "location": "North Campus",
        "organizer": "Outreach Team",
        "attendees": 60,
    },
]

DEMO_MEETINGS = [
    {
        "meeting_id": "MEE-001",
        "title": "Quarterly Budget Review",
        "category": "scheduled",
        "status": "upcoming",
        "scheduled_at": "2026-05-18T14:00:00",
        "location": "Conference Room A",
        "attendees": 50,
        "action_items": 6,
        "description": "Review of Q2 expenditures, proposed budget adjustments, and approval of next-quarter allocations.",
        "has_image": False,
        "image_url": "",
    },
    {
        "meeting_id": "MEE-002",
        "title": "Safety & Security Committee",
        "category": "scheduled",
        "status": "upcoming",
        "scheduled_at": "2026-05-20T10:00:00",
        "location": "Virtual - Teams Link",
        "attendees": 28,
        "action_items": 4,
        "description": "Discussion of workplace safety protocols, incident reporting, and emergency response readiness.",
        "has_image": False,
        "image_url": "",
    },
    {
        "meeting_id": "MEE-003",
        "title": "Emergency Road Repair Fund",
        "category": "scheduled",
        "status": "completed",
        "scheduled_at": "2026-05-04T15:30:00",
        "location": "Member Resources",
        "attendees": 15,
        "action_items": 3,
        "description": "Review emergency fund allocation procedures and recent claims.",
        "has_image": False,
        "image_url": "",
    },
    {
        "meeting_id": "MEE-004",
        "title": "Winter Training Planning",
        "category": "social_gathering",
        "status": "upcoming",
        "scheduled_at": "2026-05-22T13:00:00",
        "location": "Member Resources",
        "attendees": 8,
        "action_items": 2,
        "description": "Review of planned annual member training sessions and objectives.",
        "has_image": True,
        "image_url": "/image.jpg",
    },
    {
        "meeting_id": "MEE-005",
        "title": "Rural Water Main Issues",
        "category": "social_gathering",
        "status": "upcoming",
        "scheduled_at": "2026-05-24T13:00:00",
        "location": "Member Resources",
        "attendees": 12,
        "action_items": 1,
        "description": "Discussion about recent water main impacts and improvement plans.",
        "has_image": True,
        "image_url": "/image1.jpg",
    },
    {
        "meeting_id": "MEE-006",
        "title": "Member Forum",
        "category": "unlisted",
        "status": "upcoming",
        "scheduled_at": "2026-05-29T17:00:00",
        "location": "Main Hall",
        "attendees": 44,
        "action_items": 5,
        "description": "Open forum for member questions, updates, and general announcements.",
        "has_image": False,
        "image_url": "",
    },
]

DEMO_DUES = {
    "abdulazizkarim1073@gmail.com": [
        {"billing_period": "May 2026", "due_date": "2026-05-01", "amount": "50.00", "method": "Portal (VISA)", "status": "Current"},
        {"billing_period": "April 2026", "due_date": "2026-04-01", "amount": "50.00", "method": "Auto-Debit", "status": "Paid"},
        {"billing_period": "March 2026", "due_date": "2026-03-01", "amount": "50.00", "method": "Auto-Debit", "status": "Paid"},
        {"billing_period": "February 2026", "due_date": "2026-02-01", "amount": "50.00", "method": "Auto-Debit", "status": "Paid"},
    ],
    "test1778200286@example.com": [
        {"billing_period": "May 2026", "due_date": "2026-05-01", "amount": "45.00", "method": "Manual", "status": "Overdue"},
        {"billing_period": "April 2026", "due_date": "2026-04-01", "amount": "45.00", "method": "Manual", "status": "Paid"},
    ],
    "ruth.miles@example.org": [
        {"billing_period": "May 2026", "due_date": "2026-05-01", "amount": "45.00", "method": "Auto-Debit", "status": "Current"},
        {"billing_period": "April 2026", "due_date": "2026-04-01", "amount": "45.00", "method": "Auto-Debit", "status": "Paid"},
    ],
    "maya.choi@example.org": [
        {"billing_period": "May 2026", "due_date": "2026-05-01", "amount": "55.00", "method": "Cash", "status": "Paid"},
        {"billing_period": "April 2026", "due_date": "2026-04-01", "amount": "55.00", "method": "Cash", "status": "Paid"},
    ],
    "samuel.lee@example.org": [
        {"billing_period": "May 2026", "due_date": "2026-05-01", "amount": "45.00", "method": "Check #442", "status": "Overdue"},
        {"billing_period": "April 2026", "due_date": "2026-04-01", "amount": "45.00", "method": "Check #442", "status": "Overdue"},
    ],
    "linda.green@example.org": [
        {"billing_period": "May 2026", "due_date": "2026-05-01", "amount": "50.00", "method": "Portal (ACH)", "status": "Paid"},
        {"billing_period": "April 2026", "due_date": "2026-04-01", "amount": "50.00", "method": "Portal (ACH)", "status": "Paid"},
    ],
}

DEMO_STANDING = {
    "abdulazizkarim1073@gmail.com": {"active_since_years": 1, "payment_rate": 98, "status_label": "EXCELLENT", "current_balance": "0.00"},
    "test1778200286@example.com": {"active_since_years": 0, "payment_rate": 72, "status_label": "AT RISK", "current_balance": "45.00"},
    "ruth.miles@example.org": {"active_since_years": 2, "payment_rate": 94, "status_label": "EXCELLENT", "current_balance": "0.00"},
    "maya.choi@example.org": {"active_since_years": 1, "payment_rate": 89, "status_label": "GOOD", "current_balance": "0.00"},
    "samuel.lee@example.org": {"active_since_years": 1, "payment_rate": 68, "status_label": "AT RISK", "current_balance": "45.00"},
    "linda.green@example.org": {"active_since_years": 3, "payment_rate": 96, "status_label": "EXCELLENT", "current_balance": "0.00"},
}

DEMO_ASSIGNMENTS = {
    "abdulazizkarim1073@gmail.com": ["Safety Certified", "Mentor Training"],
    "test1778200286@example.com": ["Weekly Meetings"],
    "ruth.miles@example.org": ["Senior Field Specialist", "Safety Level IV"],
}

DEMO_CERTIFICATIONS = {
    "abdulazizkarim1073@gmail.com": [
        {"title": "Safety Level IV", "issued_by": "Safety Committee", "issued_on": "2024-02-14", "expires_on": None},
        {"title": "Mentor Training", "issued_by": "Board of Directors", "issued_on": "2024-08-21", "expires_on": None},
    ],
    "test1778200286@example.com": [
        {"title": "Meeting Facilitation", "issued_by": "Secretariat", "issued_on": "2024-11-01", "expires_on": None},
    ],
    "ruth.miles@example.org": [
        {"title": "Senior Field Specialist", "issued_by": "Operations Team", "issued_on": "2023-06-15", "expires_on": None},
        {"title": "Safety Level IV", "issued_by": "Safety Committee", "issued_on": "2024-01-20", "expires_on": None},
    ],
}

DEMO_ATTENDANCE = {
    "abdulazizkarim1073@gmail.com": [
        {"activity_id": "ACT-001", "status": "Attended", "attended_on": "2024-12-15"},
        {"activity_id": "ACT-003", "status": "Missed", "attended_on": "2023-12-08"},
    ],
    "test1778200286@example.com": [
        {"activity_id": "ACT-002", "status": "Attended", "attended_on": "2024-12-20"},
    ],
}


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def parse_datetime(value):
    return timezone.make_aware(datetime.strptime(value, "%Y-%m-%dT%H:%M:%S"))


class Command(BaseCommand):
    help = "Seed full demo data for members, dues, activities, assignments, certifications, and attendance."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete the seeded demo records before recreating them.",
        )

    def handle(self, *args, **options):
        clear = options["clear"]
        emails = [item["email"] for item in DEMO_USERS]
        activity_ids = [item["activity_id"] for item in DEMO_ACTIVITIES]
        meeting_ids = [item["meeting_id"] for item in DEMO_MEETINGS]

        if clear:
            ActivityAttendance.objects.filter(member__email__in=emails).delete()
            DuesPayment.objects.filter(member__email__in=emails).delete()
            MemberStanding.objects.filter(member__email__in=emails).delete()
            MemberAssignment.objects.filter(member__email__in=emails).delete()
            MemberCertification.objects.filter(member__email__in=emails).delete()
            Activity.objects.filter(activity_id__in=activity_ids).delete()
            Meeting.objects.filter(meeting_id__in=meeting_ids).delete()
            self.stdout.write(self.style.WARNING("Cleared existing demo records."))

        users = {}
        created_users = 0
        for payload in DEMO_USERS:
            defaults = {
                "username": payload["email"],
                "first_name": payload["full_name"].split(" ", 1)[0],
                "last_name": payload["full_name"].split(" ", 1)[1] if " " in payload["full_name"] else "",
                "role": payload["role"],
                "phone": payload["phone"],
                "avatar_url": payload["avatar_url"],
            }
            user, created = User.objects.update_or_create(
                email=payload["email"],
                defaults=defaults,
            )
            if created:
                user.set_password(payload["password"])
                created_users += 1
            else:
                user.set_password(payload["password"])
            user.save()
            users[payload["email"]] = user
            self.stdout.write(self.style.SUCCESS(f"Seeded user: {payload['email']}"))

        activities = {}
        for payload in DEMO_ACTIVITIES:
            activity, _ = Activity.objects.update_or_create(
                activity_id=payload["activity_id"],
                defaults={
                    "title": payload["title"],
                    "status": payload["status"],
                    "scheduled_at": parse_datetime(payload["scheduled_at"]),
                    "location": payload["location"],
                    "organizer": payload["organizer"],
                    "attendees": payload["attendees"],
                },
            )
            activities[payload["activity_id"]] = activity
            self.stdout.write(self.style.SUCCESS(f"Seeded activity: {payload['activity_id']}"))

        for payload in DEMO_MEETINGS:
            Meeting.objects.update_or_create(
                meeting_id=payload["meeting_id"],
                defaults={
                    "title": payload["title"],
                    "category": payload["category"],
                    "status": payload["status"],
                    "scheduled_at": parse_datetime(payload["scheduled_at"]),
                    "location": payload["location"],
                    "attendees": payload["attendees"],
                    "action_items": payload["action_items"],
                    "description": payload["description"],
                    "has_image": payload["has_image"],
                    "image_url": payload["image_url"],
                },
            )
            self.stdout.write(self.style.SUCCESS(f"Seeded meeting: {payload['meeting_id']}"))

        for email, standing_payload in DEMO_STANDING.items():
            MemberStanding.objects.update_or_create(
                member=users[email],
                defaults={
                    "active_since_years": standing_payload["active_since_years"],
                    "payment_rate": standing_payload["payment_rate"],
                    "status_label": standing_payload["status_label"],
                    "current_balance": Decimal(standing_payload["current_balance"]),
                },
            )

        for email, assignment_titles in DEMO_ASSIGNMENTS.items():
            for title in assignment_titles:
                MemberAssignment.objects.update_or_create(
                    member=users[email],
                    title=title,
                    defaults={
                        "description": "",
                        "assigned_on": parse_date("2024-01-01"),
                        "is_active": True,
                    },
                )

        for email, certification_payloads in DEMO_CERTIFICATIONS.items():
            for cert in certification_payloads:
                MemberCertification.objects.update_or_create(
                    member=users[email],
                    title=cert["title"],
                    defaults={
                        "issued_by": cert["issued_by"],
                        "issued_on": parse_date(cert["issued_on"]),
                        "expires_on": parse_date(cert["expires_on"]) if cert["expires_on"] else None,
                        "is_active": True,
                    },
                )

        for email, dues_rows in DEMO_DUES.items():
            for row in dues_rows:
                DuesPayment.objects.update_or_create(
                    member=users[email],
                    billing_period=row["billing_period"],
                    defaults={
                        "due_date": parse_date(row["due_date"]),
                        "amount": Decimal(row["amount"]),
                        "method": row["method"],
                        "status": row["status"],
                        "paid_on": parse_date(row["due_date"]),
                    },
                )

        for email, attendance_rows in DEMO_ATTENDANCE.items():
            for row in attendance_rows:
                ActivityAttendance.objects.update_or_create(
                    member=users[email],
                    activity=activities[row["activity_id"]],
                    defaults={
                        "status": row["status"],
                        "attended_on": parse_date(row["attended_on"]),
                    },
                )

        self.stdout.write(self.style.SUCCESS(f"Demo data seed complete. {created_users} users created or updated."))
