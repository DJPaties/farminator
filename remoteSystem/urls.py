from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.RegisterSystem.as_view(),name='register_system'),
    path('auth_system/',views.AuthenticateSystem.as_view(),name="auth_system"),
    path("check_data/",views.CheckRemoteSystem.as_view(),name='checkflag'),
    path('sendData/',views.GetInstantDataSystem.as_view(),name='instantData'),
    path("checktokenRaspi/",views.CheckFlagSystem.as_view(),name="checkToken"),
    path("setcontrols/",views.CheckControlSystem.as_view(),name="setcondition"),
    path('execDone/',views.ControlExecute.as_view(),name="execControl"),
    path('setConditions/',views.CheckConditionSystem.as_view(),name="setConditions"),
    path("saveConditions/",views.ConditionSet.as_view(),name="conditionSaved")

]
