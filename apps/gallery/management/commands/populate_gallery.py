from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.gallery.models import GalleryMedia
from apps.accounts.models import User
from apps.activities.models import Activity


class Command(BaseCommand):
    help = 'Create sample gallery media for testing'

    def handle(self, *args, **options):
        # Get or create a test user
        user, _ = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'username': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'super_admin',
            }
        )

        # Get first activity or None
        activity = Activity.objects.first()

        # Create sample gallery items
        sample_media = [
            {
                'title': 'Annual General Assembly',
                'description': 'Highlights from our annual general assembly meeting',
                'media_type': 'image',
                'media_file': 'gallery/sample1.jpg',
                'date_taken': timezone.now() - timedelta(days=30),
            },
            {
                'title': 'Community Outreach Event',
                'description': 'Our recent community outreach initiative',
                'media_type': 'image',
                'media_file': 'gallery/sample2.jpg',
                'date_taken': timezone.now() - timedelta(days=25),
            },
            {
                'title': 'Training Session',
                'description': 'Training session for new members',
                'media_type': 'video',
                'media_file': 'gallery/sample3.mp4',
                'date_taken': timezone.now() - timedelta(days=20),
            },
            {
                'title': 'Leadership Meeting',
                'description': 'Monthly leadership meeting',
                'media_type': 'image',
                'media_file': 'gallery/sample4.jpg',
                'date_taken': timezone.now() - timedelta(days=15),
            },
            {
                'title': 'Member Celebration',
                'description': 'Celebrating member achievements',
                'media_type': 'image',
                'media_file': 'gallery/sample5.jpg',
                'date_taken': timezone.now() - timedelta(days=10),
            },
            {
                'title': 'Workshop Recording',
                'description': 'Recording from our recent workshop',
                'media_type': 'video',
                'media_file': 'gallery/sample6.mp4',
                'date_taken': timezone.now() - timedelta(days=5),
            },
        ]

        for media_data in sample_media:
            GalleryMedia.objects.get_or_create(
                title=media_data['title'],
                defaults={
                    'description': media_data['description'],
                    'media_type': media_data['media_type'],
                    'media_file': media_data['media_file'],
                    'date_taken': media_data['date_taken'],
                    'uploaded_by': user,
                    'activity': activity,
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully created sample gallery media'))
