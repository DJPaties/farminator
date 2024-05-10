
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django.urls import path

urlpatterns = [
    # path('validate_token/',views.CustomUserValidateToken.as_view(),name="validate_token"),
    path("login/", views.CustomObtainAuthToken.as_view(), name="login"),
    path("logout_user/", views.UserLogoutView.as_view(), name="logout_user"),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    # path("getuser/",views.get_user_token,name='getUser')
]
