from django import forms
from .models import Job, Category
from django_select2.forms import ModelSelect2Widget

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'job_type', 'company_awards_recognitions', 
                  'schedule', 'career_level', 'education_level', 
                  'category', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'company_awards_recognitions': forms.TextInput(attrs={'class': 'form-control'}),
            'schedule': forms.Select(attrs={'class': 'form-control'}),
            'career_level': forms.Select(attrs={'class': 'form-control'}),
            'education_level': forms.TextInput(attrs={'class': 'form-control'}),
            'category': ModelSelect2Widget(
                model=Category,
                search_fields=['name__icontains'],
                attrs={'class': 'form-control'}  # Adding Bootstrap class for styling
            ),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
