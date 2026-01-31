from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, AdminLoginForm


def signup_view(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('accounts:redirect_dashboard')
    return render(request, 'auth/signup.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user and user.role in ['fresher', 'recruiter']:
            login(request, user)
            return redirect('accounts:redirect_dashboard')
        return render(request, 'auth/login.html', {
            'form': form,
            'error': 'Invalid credentials'
        })
    return render(request, 'auth/login.html', {'form': form})



def admin_login_view(request):

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('/admin-panel/dashboard/')

    if request.method == 'POST':
        form = AdminLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user and user.is_superuser:
                login(request, user)
                return redirect('/admin-panel/dashboard/')
            else:
                error = "Invalid admin credentials"
        else:
            error = "Invalid input"

        return render(request, 'auth/admin_login.html', {
            'form': form,
            'error': error
        })

    form = AdminLoginForm()
    return render(request, 'auth/admin_login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def redirect_dashboard(request):
    if request.user.role == 'fresher':
        return redirect('/freshers/dashboard/')
    elif request.user.role == 'recruiter':
        return redirect('/recruiters/dashboard/')
    elif request.user.role == 'admin':
        return redirect('/admin-panel/dashboard/')
