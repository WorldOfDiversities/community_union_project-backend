from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

SAMPLE = [
    ("alex.brown@example.org", "Alex Brown", "admin", "/image.jpg"),
    ("james.howard@example.org", "James Howard", "treasurer", "/image1.jpg"),
    ("ruth.miles@example.org", "Ruth Miles", "secretary", "/image2.jpg"),
    ("linda.green@example.org", "Linda Green", "member", "/image3.jpg"),
    ("samuel.lee@example.org", "Samuel Lee", "member", "/image5.jpg"),
    ("maya.choi@example.org", "Maya Choi", "member", "/image6.jpg"),
]

class Command(BaseCommand):
    help = 'Seed sample users with avatar URLs'

    def handle(self, *args, **options):
        created = 0
        for email, full_name, role, avatar in SAMPLE:
            name_parts = full_name.split(' ', 1)
            first = name_parts[0]
            last = name_parts[1] if len(name_parts) > 1 else ''
            normalized_role = 'member' if role == 'member' else 'executive' if role == 'treasurer' else role
            user = User.objects.filter(email__iexact=email).first()
            created_flag = user is None
            if created_flag:
                user = User.objects.create(
                    username=email,
                    email=email,
                    first_name=first,
                    last_name=last,
                    role=normalized_role,
                )
                user.set_password('Password123!')
            else:
                user.username = email
                user.email = email
                user.first_name = first
                user.last_name = last
                user.role = normalized_role
            user.avatar_url = avatar
            user.save()
            created += 1 if created_flag else 0
            self.stdout.write(self.style.SUCCESS(f"Updated {email}" if not created_flag else f"Created {email}"))
        self.stdout.write(self.style.SUCCESS(f"Seeding complete. {created} users created."))
