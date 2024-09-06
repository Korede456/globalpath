from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from account.forms import EmployerSignupForm
from account.models import CustomUser
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DeleteView
from .models import Job
from django.utils.decorators import method_decorator
from .forms import JobForm

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
    return render(request, "employer/employer_home.html")


@login_required
def dashboard(request):
    if request.user.role == CustomUser.Role.EMPLOYER:
        return render(request, "employer/dashboard.html")
    else:
        return HttpResponseForbidden("You do not have permission to access this page.")


# Employer can create post
@method_decorator(login_required, name='dispatch')
class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = 'template.html'
    template_name = 'employer/job_post_form.html' # you should change this based on what you are creating .
    success_url = reverse_lazy('employer:dashboard')


    def form_valid(self, form):
        if self.request.user.role == CustomUser.Role.EMPLOYER:
            form.instance.user = self.request.user.employerprofile
            return super().form_valid(form)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")


@method_decorator(login_required, name='dispatch')
class DeleteJobs(DeleteView):
    model = Job
    template_name = 'employer/job_confirm_delete.html' 
    success_url = reverse_lazy('employer:dashboard')
    
    
    # this get_queryset() is part of Django builtIn Class based view(CBVs),
    # it is responsible for determining the set of objects that the view will wok with
    
    """
    down here, the objects if filltered before the view tries to act on it, if thw usr isn't auth.., they'll get a 404 error
    """
    def get_queryset(self):   
        " Ensure that only the employer who posted the job can delete it "
        query = super().get_queryset()
        print(query) # for debugging
        
        if self.request.user.role == CustomUser.Role.EMPLOYER:
            return query.filter(user=self.request.user.employerprofile)
        else:
            return Job.objects.none()
        
    def delete(self, request, *args, **kwargs):
        """ custom delete method to handle permissions or other pre-deleted actions """
        if self.request.user.role  != CustomUser.Role.EMPLOYER:
            return HttpResponseForbidden("You do not have permission to access this page.")
        else:
            return super().delete(request, *args, **kwargs)
        