# myshop/middleware.py

from django.conf import settings
from django.urls import reverse


class CustomAuthRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Default URLs
        login_url = "/login/"
        login_redirect_url = "/"
        logout_redirect_url = "/"

        # Check request path to determine the appropriate app
        if request.path.startswith("/jobseeker/"):
            login_url = reverse("jobseeker:signin")
            login_redirect_url = "/"  # Change to your desired URL
            logout_redirect_url = "/"

        elif request.path.startswith("/member/"):
            login_url = reverse("employer:signin")
            login_redirect_url = reverse(
                "employer:dashboard"
            )  # Change to your desired URL
            logout_redirect_url = "/"

        # Set the dynamic URLs in the settings
        request.login_url = login_url
        request.login_redirect_url = login_redirect_url
        request.logout_redirect_url = logout_redirect_url

        # Update settings dynamically
        settings.LOGIN_URL = login_url
        settings.LOGIN_REDIRECT_URL = login_redirect_url
        settings.LOGOUT_REDIRECT_URL = logout_redirect_url

        # Call the next middleware or view
        response = self.get_response(request)
        return response
