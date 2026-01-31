from django.contrib import admin
from .models import Job
# Register your models here.

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'is_open', 'created_at')
    list_filter = ('is_open',)

admin.site.register(Job, JobAdmin)