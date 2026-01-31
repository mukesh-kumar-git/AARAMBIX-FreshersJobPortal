from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm
from recruiters.models import RecruiterProfile

# Create your views here.

def recruiter_required(user):
    return user.is_authenticated and user.role.lower() == 'recruiter'

def job_list(request):
    """
    Show all OPEN jobs to freshers.
    Optional search by job title.
    """
    query = request.GET.get('q')
    jobs = Job.objects.filter(is_open=True)
    if query:
        jobs = jobs.filter(title__icontains=query)
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def job_detail(request, job_id):
    """
    Show single job details (only if job is open)
    """
    job = get_object_or_404(Job, id=job_id, is_open=True)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def recruiter_jobs(request):
    if not recruiter_required(request.user):
        return redirect('accounts:login')
    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, 'jobs/recruiter_jobs.html', {'jobs': jobs})


@login_required
def create_job(request):
    if not recruiter_required(request.user):
        return redirect('accounts:login')

    # Check recruiter approval
    profile = RecruiterProfile.objects.filter(
        user=request.user,
        is_approved=True
    ).first()
    if not profile:
        return redirect('recruiters:approval_status')
    form = JobForm(request.POST or None)
    if form.is_valid():
        job = form.save(commit=False)
        job.recruiter = request.user
        job.save()
        return redirect('jobs:recruiter_jobs')
    return render(request, 'jobs/job_form.html', {'form': form,'action': 'Create'})


@login_required
def edit_job(request, job_id):
    if not recruiter_required(request.user):
        return redirect('accounts:login')
    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=request.user
    )
    form = JobForm(request.POST or None, instance=job)
    if form.is_valid():
        form.save()
        return redirect('jobs:recruiter_jobs')
    return render(request, 'jobs/job_form.html', {'form': form,'action': 'Edit'})