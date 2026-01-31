from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my-applications/', views.fresher_applications, name='fresher_applications'),
    path('recruiter/<int:job_id>/', views.recruiter_applications, name='recruiter_applications'),
    path('update-status/<int:app_id>/', views.update_status, name='update_status'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
]