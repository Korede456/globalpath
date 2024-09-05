from django import forms
from .models import Job


class jobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'job_type', 'company', 'company_awards_recongnitions',
                  'schedule', 'career_level', 'education_level', 'category',
                  'description']
        
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'job_type': forms.Select(attrs={'class' : 'form-control'}),
            'company': forms.Select(attrs={'class' : 'form-control'}),
            'company_awards_recongnitions': forms.Select(attrs={'class' : 'form-control'}),
            'schedule': forms.Select(attrs={'class' : 'form-control'}),
            'career_level': forms.Select(attrs={'class' : 'form-control'}),
            'education_level' : forms.TextInput(attrs={'class': 'form-control'}),
            'category' : forms.Select(attrs=({'class': 'form-control'})),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),
        }
        