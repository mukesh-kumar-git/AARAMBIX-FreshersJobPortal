from django import forms
from .models import RecruiterProfile, Company


class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ["phone", "designation"]
        widgets = {
            "phone": forms.TextInput(attrs={
                "placeholder": "Phone number"
            }),
            "designation": forms.TextInput(attrs={
                "placeholder": "Your designation (HR, Manager, etc.)"
            }),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "description", "website", "location"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Company name"
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Describe your company"
            }),
            "website": forms.URLInput(attrs={
                "placeholder": "https://companywebsite.com"
            }),
            "location": forms.TextInput(attrs={
                "placeholder": "Company location"
            }),
        }
