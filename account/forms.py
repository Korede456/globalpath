from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Employer, EmployerProfile, Jobseeker


class EmployerSignupForm(UserCreationForm):
    job_title = forms.CharField(max_length=50, required=True)
    company_name = forms.CharField(max_length=50, required=True)
    company_web_address = forms.URLField(max_length=50, required=True)

    class Meta:
        model = Employer  # Use the Employer model
        fields = (
            "email",
            "first_name",
            "last_name",
            "job_title",
            "company_name",
            "company_web_address",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.Role.EMPLOYER
        if commit:
            user.save()
            EmployerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data["company_name"],
                company_web_address=self.cleaned_data["company_web_address"],
            )
        return user


class JobseekerSignupForm(UserCreationForm):
    class Meta:
        model = Jobseeker  # Use the Jobseeker model
        fields = ("email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.Role.JOBSEEKER
        if commit:
            user.save()
        return user
