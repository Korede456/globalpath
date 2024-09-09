from django.urls import path
from .views import SignupView, SigninView, SignoutView, home, JobListingsView

app_name = "jobseeker"
urlpatterns = [
    path("", home, name="home"),
    path("jobseeker/signup/", SignupView.as_view(), name="signup"),
    path("jobseeker/signin/", SigninView.as_view(), name="signin"),
    path("jobseeker/signout/", SignoutView.as_view(), name="signout"),
    path("jobseeker/find-jobs/", JobListingsView.as_view(), name="find-job")
]
