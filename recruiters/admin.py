from django.contrib import admin
from .models import RecruiterProfile, Company

# Register your models here.

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'phone', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('user__username',)
    list_display = ("user", "phone", "designation", "is_approved", "rejected")
    list_filter = ("is_approved", "rejected")
    search_fields = ("user__username",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    search_fields = ('name',)
    list_display = ("name", "location", "recruiter")
