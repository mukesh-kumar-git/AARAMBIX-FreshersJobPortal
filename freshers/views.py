from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import FresherProfile, Resume
from .forms import FresherProfileForm, ResumeUploadForm
from applications.models import JobApplication
from jobs.models import Job


def fresher_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'fresher':
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@fresher_required
def dashboard(request):
    query = request.GET.get('q')

    jobs = Job.objects.filter(is_open=True)

    if query:
        jobs = jobs.filter(
            title__icontains=query
        ) | jobs.filter(
            company_name__icontains=query
        ) | jobs.filter(
            skills_required__icontains=query
        )

    profile = FresherProfile.objects.filter(user=request.user).first()
    resume = Resume.objects.filter(fresher=request.user).first()
    applications = JobApplication.objects.filter(fresher=request.user)

    return render(request, 'freshers/dashboard.html', {
        'jobs': jobs,
        'profile': profile,
        'resume': resume,
        'applications': applications,
    })


@login_required
@fresher_required
def profile_view(request):
    profile, _ = FresherProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = FresherProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('freshers:dashboard')
    else:
        form = FresherProfileForm(instance=profile)

    return render(request, 'freshers/profile.html', {'form': form})


@login_required
@fresher_required
def upload_resume(request):
    resume = Resume.objects.filter(fresher=request.user).first()

    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES, instance=resume)

        if form.is_valid():
            uploaded_file = request.FILES.get('resume')

            if uploaded_file and not uploaded_file.name.endswith('.pdf'):
                return render(request, 'freshers/resume_upload.html', {
                    'form': form,
                    'error': 'Only PDF files are allowed'
                })

            resume = form.save(commit=False)
            resume.fresher = request.user
            resume.save()
            return redirect('freshers:dashboard')
    else:
        form = ResumeUploadForm(instance=resume)

    return render(request, 'freshers/resume_upload.html', {'form': form})


@login_required
@fresher_required
def applied_jobs(request):
    applications = JobApplication.objects.filter(fresher=request.user)
    return render(request, 'freshers/applied_jobs.html', {
        'applications': applications
    })
