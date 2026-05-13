from django.db import models
from apps.accounts.models import BaseModel, User
from apps.activities.models import Activity


class GalleryMedia(BaseModel):
    """Model for storing gallery media (images and videos)."""
    
    MEDIA_TYPE_CHOICES = [
        ("image", "Image"),
        ("video", "Video"),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    media_file = models.FileField(upload_to='gallery/%Y/%m/%d/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, blank=True, null=True, related_name="gallery_media")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_taken = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = "gallery_media"
        ordering = ["-date_taken", "-created_at"]
        verbose_name = "Gallery Media"
        verbose_name_plural = "Gallery Media"
    
    def __str__(self):
        return f"{self.title} ({self.media_type})"
