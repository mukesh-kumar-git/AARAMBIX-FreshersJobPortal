from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import RecruiterProfile, Company
from .forms import CompanyForm
from jobs.models import Job
from applications.models import JobApplication


def recruiter_required(user):
    return (
        user.is_authenticated and
        hasattr(user, "recruiter_profile") and
        user.recruiter_profile.is_approved
    )


@login_required
def recruiter_dashboard(request):
    if not recruiter_required(request.user):
        return HttpResponseForbidden("Access denied")

    jobs = Job.objects.filter(recruiter=request.user)

    company = getattr(
        request.user.recruiter_profile,
        "company",
        None
    )

    return render(request, "recruiters/dashboard.html", {
        "jobs": jobs,
        "company": company
    })


@login_required
def company_profile(request):
    if not recruiter_required(request.user):
        return HttpResponseForbidden("Access denied")

    recruiter_profile = request.user.recruiter_profile

    company, created = Company.objects.get_or_create(
        recruiter=recruiter_profile
    )

    form = CompanyForm(request.POST or None, instance=company)

    if form.is_valid():
        form.save()
        return redirect("recruiters:dashboard")

    return render(request, "recruiters/company_form.html", {
        "form": form,
        "company": company
    })


@login_required
def job_applications(request, job_id):
    if not recruiter_required(request.user):
        return HttpResponseForbidden("Access denied")

    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=request.user
    )

    applications = job.applications.all()

    return render(request, "recruiters/job_applications.html", {
        "job": job,
        "applications": applications
    })


@login_required
def update_application_status(request, app_id, status):
    if not recruiter_required(request.user):
        return HttpResponseForbidden("Access denied")

    application = get_object_or_404(
        JobApplication,
        id=app_id,
        job__recruiter=request.user
    )

    if status in ["shortlisted", "rejected", "hired"]:
        application.status = status
        application.save()

    return redirect(
        "recruiters:job_applications",
        job_id=application.job.id
    )
