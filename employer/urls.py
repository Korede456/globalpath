from django.urls import path
from .views import SignupView, SigninView, SignoutView, employer_home, dashboard

app_name = "employer"
urlpatterns = [
    path("home/", employer_home, name="home"),
    path("dashbaord", dashboard, name="dashboard"),
    path("register/", SignupView.as_view(), name="signup"),
    path("signin/", SigninView.as_view(), name="signin"),
    path("signout/", SignoutView.as_view(), name="signout"),
]
