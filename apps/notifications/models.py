from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


def default_announcement_expiry():
    return timezone.now() + timedelta(days=7)


class Announcement(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_announcements'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_announcement_expiry)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = default_announcement_expiry()
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.expires_at and self.expires_at <= timezone.now()

    def __str__(self):
        return f"Announcement: {self.subject}"


# TODO: Create Notification models here
