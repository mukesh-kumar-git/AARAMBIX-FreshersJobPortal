from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class RecruiterProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recruiter_profile"
    )

    phone = models.CharField(max_length=15)
    designation = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Company(models.Model):
    recruiter = models.OneToOneField(
        RecruiterProfile,
        on_delete=models.CASCADE,
        related_name="company"
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
