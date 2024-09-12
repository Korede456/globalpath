from django.urls import path
from .views import *
app_name = "employer"
urlpatterns = [
    path("home/", employer_home, name="home"),
    path("dashboard", dashboard, name="dashboard"),
    path("register/", SignupView.as_view(), name="signup"),
    path("signin/", SigninView.as_view(), name="signin"),
    path("signout/", SignoutView.as_view(), name="signout"),
    path("post_job/", JobCreateView.as_view(), name="post_job"),
    path("delete/<int:job_id>", delete_job, name="job_delete"),
    path("job/edit/<int:job_id>/", JobEditView.as_view(), name="job_edit"),
    path("about/", about_us, name="about_us"),
]
