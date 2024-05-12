from django.urls import path  # Import the path function from Django's URL module.
from rest_framework.authtoken.views import obtain_auth_token  # Import the obtain_auth_token view from Django REST framework.
from . import views  # Import views from the current directory.

urlpatterns = [
    path("login/", views.CustomObtainAuthToken.as_view(), name="login"),  # Route login requests to the CustomObtainAuthToken view.
    path("logout_user/", views.UserLogoutView.as_view(), name="logout_user"),  # Route logout requests to the UserLogoutView view.
    path("register/", views.UserRegistrationView.as_view(), name="register"),  # Route registration requests to the UserRegistrationView view.

    path('validate-token/', views.ValidateTokenView.as_view(), name='validate_token'),  # Route token validation requests to the ValidateTokenView view.
]