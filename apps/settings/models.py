from django.db import models


class OrganizationSettings(models.Model):
    """Global settings for the union organization."""
    
    union_name = models.CharField(max_length=255, default='Community Union Africa')
    chapter_number = models.CharField(max_length=50, default='0104')
    primary_contact_email = models.EmailField(default='admin@communityunion.africa')
    time_zone = models.CharField(max_length=100, default='Eastern Standard Time (EST)')
    
    physical_address = models.TextField(default='324 Madaraka Ave, Accra, Ghana')
    chapter_details = models.TextField(default='Wungu Regional Office | EST: 5:00 PM')
    logo = models.FileField(upload_to='logos/', blank=True, null=True)
    
    # Notification preferences
    dues_sms_enabled = models.BooleanField(default=False)
    dues_email_enabled = models.BooleanField(default=True)
    meeting_sms_enabled = models.BooleanField(default=False)
    meeting_email_enabled = models.BooleanField(default=True)
    member_updates_sms_enabled = models.BooleanField(default=False)
    member_updates_email_enabled = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Organization Settings'
        verbose_name_plural = 'Organization Settings'
    
    def __str__(self):
        return f'{self.union_name} Settings'
