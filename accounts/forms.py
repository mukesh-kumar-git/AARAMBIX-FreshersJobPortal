from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
from .models import CustomUser


# Fresher & Recruiter Signup
class SignupForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            ('fresher', 'Fresher'),
            ('recruiter', 'Recruiter'),
        ]
    )
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']


# Fresher & Recruiter Login
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()


# Admin Login
class AdminLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    #captcha = CaptchaField()
