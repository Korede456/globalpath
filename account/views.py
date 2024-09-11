from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, View, TemplateView
from .forms import JobseekerSignupForm
from .models import CustomUser


class SignupView(FormView):
    template_name = "jobseeker/signup.html"
    form_class = JobseekerSignupForm  # Use the specific Jobseeker form
    success_url = reverse_lazy("jobseeker:signin")

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
            return redirect('employer:home')

    # Render the jobseeker home page for non-logged-in users or jobseekers
    return render(request, "jobseeker/home.html")


def about_us(request):
    
    # Render the jobseeker home page for non-logged-in users or jobseekers
    return render(request, "jobseeker/about_us.html")
