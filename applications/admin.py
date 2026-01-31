from django.contrib import admin
from .models import JobApplication

# Register your models here.

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'fresher', 'status', 'applied_at')
    list_filter = ('status',)
admin.site.register(JobApplication, JobApplicationAdmin)