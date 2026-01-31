from django.db import models
from django.conf import settings


class Job(models.Model):
    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    skills_required = models.CharField(max_length=300)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_applications(self):
        return self.applications.count()

    def __str__(self):
        return self.title
