from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class SystemAuditLog(models.Model):
    SEVERITY_CHOICES = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('CRITICAL', 'Critical'),
    ]

    event_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='INFO')

    def __str__(self):
        return f"[{self.severity}] {self.event_name} at {self.timestamp}"