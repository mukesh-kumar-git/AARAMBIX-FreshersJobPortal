from django.contrib import admin
from .models import FresherProfile, Resume, JobApplication


class FresherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'education')


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('fresher',)


admin.site.register(FresherProfile, FresherProfileAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(JobApplication)
