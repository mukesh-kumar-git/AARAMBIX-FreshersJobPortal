from django import forms
from .models import FresherProfile, Resume


class FresherProfileForm(forms.ModelForm):
    class Meta:
        model = FresherProfile
        fields = ['education', 'skills', 'bio']


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if not file.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed")

        if file.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Resume file must be under 2MB")

        return file
