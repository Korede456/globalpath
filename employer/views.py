from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from account.forms import EmployerSignupForm
from account.models import CustomUser
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .models import Job, Category
from django.utils.decorators import method_decorator
from .forms import JobForm
from django.utils import timezone

class SignupView(FormView):
    template_name = "employer/signup.html"  # Update the template to employer signup
    form_class = EmployerSignupForm  # Use the specific Employer form
    success_url = reverse_lazy("employer:signin")

    def form_valid(self, form):
        form.save()  # Save the employer user
        return redirect(self.get_success_url())


class SigninView(FormView):
    template_name = "employer/signin.html"  # Update the template to employer signin
    form_class = AuthenticationForm
    success_url = reverse_lazy("employer:dashboard")

    def form_valid(self, form):
        email = form.cleaned_data.get("username")  # Using 'username' field for email
        password = form.cleaned_data.get("password")

        # Authenticate using the default backend
        user = authenticate(
            self.request,
            username=email,
            password=password,
        )

        if user is not None:
            if user.role == CustomUser.Role.EMPLOYER:  # Ensure the user is an Employer
                login(self.request, user)
                return redirect(self.get_success_url())
            else:
                form.add_error(None, "This sign-in page is only for employers.")
        else:
            form.add_error(None, "Invalid email or password.")

        return self.form_invalid(form)


class SignoutView(View):
    def get(self, request):
        logout(request)
        return redirect("employer:home")  # Update 'home' to your desired URL name


def employer_home(request):
    # Check if the user is logged in
    if request.user.is_authenticated:
        # If the user is not an employer, redirect them to the jobseeker home page
        if request.user.role != CustomUser.Role.EMPLOYER:
            return redirect('jobseeker:home')

    # Render the employer home page for non-logged-in users or employers
    return render(request, "employer/employer_home.html")


@login_required
def dashboard(request):
    categories = Category.objects.all()

    if request.user.role == CustomUser.Role.EMPLOYER:
        # Fetch jobs posted by the logged-in employer
        employer_profile = request.user.employerprofile
        jobs = Job.objects.filter(company=employer_profile)
        today = timezone.now().date()
        
        # Pass categories and jobs to the template context
        return render(request, "employer/dashboard.html", {'categories': categories, 'jobs': jobs, 'today': today})
    else:
        return HttpResponseForbidden("You do not have permission to access this page.")



# Employer can create post
@method_decorator(login_required, name='dispatch')
class JobCreateView(FormView):
    template_name = 'employer/job_form.html'
    form_class = JobForm
    success_url = reverse_lazy('employer:dashboard')  # Where to redirect after form submission

    def form_valid(self, form):
        # Ensure only employers can submit job posts
        if self.request.user.role == CustomUser.Role.EMPLOYER:
            employer_profile = self.request.user.employerprofile
            job = form.save(commit=False)  # Don't save the form yet
            job.company = employer_profile  # Autofill the company field
            job.save()  # Now save the form data with the company field
            return redirect(self.get_success_url())  # Redirect to success URL
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")