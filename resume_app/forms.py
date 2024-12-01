from django import forms

class ResumeUploadForm(forms.Form):
    file = forms.FileField(label='Upload Resume (PDF/Word)', required=True)
