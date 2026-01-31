from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),  # ✅ ADD THIS

    path('recruiters/', views.manage_recruiters, name='manage_recruiters'),
    path('recruiters/approve/<int:profile_id>/', views.approve_recruiter, name='approve_recruiter'),

    path('jobs/', views.manage_jobs, name='manage_jobs'),
    path('jobs/toggle/<int:job_id>/', views.toggle_job_status, name='toggle_job_status'),
]
