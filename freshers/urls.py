from django.urls import path
from . import views

app_name = 'freshers'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('resume/upload/', views.upload_resume, name='upload_resume'),
    path('applied-jobs/', views.applied_jobs, name='applied_jobs'),
]
