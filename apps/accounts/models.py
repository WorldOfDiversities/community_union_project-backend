from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    """Abstract base model with audit fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class User(AbstractUser):
    """Custom User model for CUMS."""
    ROLE_CHOICES = [
        ("super_admin", "Super Admin"),
        ("executive", "Executive"),
        ("secretary", "Secretary"),
        ("member", "Member"),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar_url = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "accounts_user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

