from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("<int:job_id>/", views.job_detail, name="job_detail"),

    # recruiter routes
    path("recruiter/my-jobs/", views.recruiter_jobs, name="recruiter_jobs"),
    path("recruiter/create/", views.create_job, name="create_job"),
    path("recruiter/edit/<int:job_id>/", views.edit_job, name="edit_job"),
]
