from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from .forms import JobseekerSignupForm
from .models import CustomUser
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.views import View
from django.contrib.auth.decorators import login_required
from employer.models import *
from django.utils import timezone

class SignupView(FormView):
    template_name = "jobseeker/signup.html"
    form_class = JobseekerSignupForm  # Use the specific Jobseeker form
    success_url = reverse_lazy("jobseeker:get_job")

    def form_valid(self, form):
        form.save()  # Save the jobseeker user
        return redirect(self.get_success_url())


class SigninView(FormView):
    template_name = "jobseeker/signin.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("jobseeker:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("username")  # Using 'username' field for email
        password = form.cleaned_data.get("password")

        # Authenticate using the custom backend for JobseekerAccount
        user = authenticate(
            self.request,
            username=email,
            password=password,
        )

        if user is not None:
            if user.role == CustomUser.Role.JOBSEEKER:  # Ensure the user is a Jobseeker
                login(self.request, user)
                return redirect(self.get_success_url())
            else:
                form.add_error(None, "This sign-in page is only for job seekers.")
        else:
            form.add_error(None, "Invalid email or password.")

        return self.form_invalid(form)


class SignoutView(View):
    def get(self, request):
        logout(request)
        return redirect("jobseeker:home")  # Update 'home' to your desired URL name


def home(request):
    # Check if the user is logged in
    if request.user.is_authenticated:
        # If the user is not a jobseeker, redirect them to the employer home page
        if request.user.role != CustomUser.Role.JOBSEEKER:
            return redirect("employer:home")

    # Render the jobseeker home page for non-logged-in users or jobseekers
    return render(request, "jobseeker/home.html")


@method_decorator(login_required, name="dispatch")
class JobListingsView(View):
    template_name = 'jobseeker/get_jobs.html'

    def get(self, request, *args, **kwargs):
        # Check if the user is a jobseeker
        if request.user.role == CustomUser.Role.JOBSEEKER:
            # Fetch all available jobs, sorted from latest to oldest
            jobs = Job.objects.all().order_by('-time_posted')

            # Handle search query
            search_query = request.GET.get('search')
            if search_query:
                jobs = jobs.filter(title__icontains=search_query)

            # Handle filters
            job_type = request.GET.get('job_type')
            if job_type:
                jobs = jobs.filter(job_type=job_type)

            schedule = request.GET.get('schedule')
            if schedule:
                jobs = jobs.filter(schedule=schedule)

            career_level = request.GET.get('career_level')
            if career_level:
                jobs = jobs.filter(career_level=career_level)

            category = request.GET.get('category')
            if category:
                jobs = jobs.filter(category__id=category)

            # Fetch all categories for the filter dropdown
            categories = Category.objects.all()

            # Get today's date for the template
            today = timezone.now().date()

            # Render the template with jobs, categories, and today's date
            return render(request, self.template_name, {
                'jobs': jobs,
                'categories': categories,
                'today': today
            })
        else:
            # If the user is not a jobseeker, deny access
            return HttpResponseForbidden('You do not have permission to view this page.')