from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import JobApplication
from jobs.models import Job

# Create your views here.

def fresher_required(user):
    return user.is_authenticated and user.role.lower() == 'fresher'

def recruiter_required(user):
    return user.is_authenticated and user.role.lower() == 'recruiter'

@login_required
def apply_job(request, job_id):
    if not fresher_required(request.user):
        return HttpResponseForbidden("Access denied")
    job = get_object_or_404(Job, id=job_id, is_open=True)

    # Prevent duplicate application
    if JobApplication.objects.filter(job=job, fresher=request.user).exists():
        return redirect('applications:fresher_applications')
    JobApplication.objects.create( job=job,fresher=request.user )
    return redirect('applications:fresher_applications')

@login_required
def fresher_applications(request):
    if not fresher_required(request.user):
        return HttpResponseForbidden("Access denied")
    applications = JobApplication.objects.filter(
        fresher=request.user
    ).order_by('-applied_at')
    return render(request, 'applications/fresher_applications.html', {'applications': applications })

@login_required
def recruiter_applications(request, job_id):
    if not recruiter_required(request.user):
        return HttpResponseForbidden("Access denied")
    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=request.user
    )
    applications = JobApplication.objects.filter(job=job)
    return render(request, 'applications/recruiter_applications.html', {
        'job': job,
        'applications': applications
    })

@login_required
def update_status(request, app_id):
    if not recruiter_required(request.user):
        return HttpResponseForbidden("Access denied")
    application = get_object_or_404(
        JobApplication,
        id=app_id,
        job__recruiter=request.user
    )
    if request.method == 'POST':
        status = request.POST.get('status')
        application.status = status
        application.save()
    return redirect(
        'applications:recruiter_applications',
        job_id=application.job.id
    )

@login_required
def apply_job(request, job_id):
    # Only freshers can apply
    if request.user.role != 'fresher':
        return HttpResponseForbidden("Only freshers can apply")

    job = get_object_or_404(Job, id=job_id, is_open=True)

    # Prevent duplicate application
    if JobApplication.objects.filter(job=job, fresher=request.user).exists():
        return redirect('freshers:applied_jobs')

    if request.method == "POST":
        JobApplication.objects.create(
            job=job,
            fresher=request.user
        )
        return redirect('freshers:applied_jobs')

    # GET request → show apply form
    return render(request, 'applications/apply_job.html', {
        'job': job
    })