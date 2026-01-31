from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class FresherProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="fresher_profile"
    )
    education = models.CharField(max_length=255)
    skills = models.TextField(help_text="Comma-separated skills")
    bio = models.TextField(blank=True)

    # Optional resume upload
    resume = models.FileField(
        upload_to='resumes/',
        null=True,
        blank=True
    )

    def profile_completion(self):
        score = 0
        if self.education:
            score += 40
        if self.skills:
            score += 40
        if self.bio:
            score += 20
        return score

    def __str__(self):
        return f"FresherProfile - {self.user}"


class Resume(models.Model):
    fresher = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="resume"
    )
    file = models.FileField(upload_to="resumes/")
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume - {self.fresher}"


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    )

    fresher = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='applied'
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fresher} → {self.job_title}"
