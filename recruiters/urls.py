from django.urls import path
from . import views

app_name = "recruiters"

urlpatterns = [
    path("dashboard/", views.recruiter_dashboard, name="dashboard"),

    path(
        "jobs/<int:job_id>/applications/",
        views.job_applications,
        name="job_applications"
    ),

    path(
        "applications/<int:app_id>/<str:status>/",
        views.update_application_status,
        name="update_application_status"
    ),

    path("company/", views.company_profile, name="company_profile"),
]
