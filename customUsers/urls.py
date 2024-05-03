
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('validate_token/',views.CustomUserValidateToken.as_view(),name="validate_token"),
    path("login/", views.CustomUserLogin.as_view(), name="login"),
    path("logout_user/", views.CustomUserLogout.as_view(), name="logout_user"),
    path("register/", views.CustomUserRegister.as_view(), name="register"),
    # path("getuser/",views.get_user_token,name='getUser')
]
