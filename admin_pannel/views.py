from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from accounts.models import CustomUser
from recruiters.models import RecruiterProfile
from jobs.models import Job
from applications.models import JobApplication


def admin_required(user):
    return user.is_authenticated and user.is_superuser




@login_required(login_url='/accounts/admin-login/')
def admin_dashboard(request):
    if not admin_required(request.user):
        return HttpResponseForbidden("Access denied")

    context = {
        'total_users': CustomUser.objects.count(),
        'total_freshers': CustomUser.objects.filter(role='fresher').count(),
        'total_recruiters': CustomUser.objects.filter(role='recruiter').count(),
        'total_jobs': Job.objects.count(),
        'total_applications': JobApplication.objects.count(),
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required(login_url='/accounts/admin-login/')
def manage_recruiters(request):
    if not admin_required(request.user):
        return HttpResponseForbidden("Access denied")

    recruiters = RecruiterProfile.objects.select_related('user')
    return render(request, 'admin_panel/recruiters.html', {'recruiters': recruiters})


@login_required(login_url='/accounts/admin-login/')
def approve_recruiter(request, profile_id):
    if not admin_required(request.user):
        return HttpResponseForbidden("Access denied")

    profile = get_object_or_404(RecruiterProfile, id=profile_id)
    profile.is_approved = True
    profile.save()
    return redirect('admin_panel:manage_recruiters')


@login_required(login_url='/accounts/admin-login/')
def manage_jobs(request):
    if not admin_required(request.user):
        return HttpResponseForbidden("Access denied")

    jobs = Job.objects.select_related('recruiter')
    return render(request, 'admin_panel/jobs.html', {'jobs': jobs})


@login_required(login_url='/accounts/admin-login/')
def toggle_job_status(request, job_id):
    if not admin_required(request.user):
        return HttpResponseForbidden("Access denied")

    job = get_object_or_404(Job, id=job_id)
    job.is_open = not job.is_open
    job.save()
    return redirect('admin_panel:manage_jobs')
