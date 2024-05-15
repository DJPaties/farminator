from django.urls import path
from . import views

urlpatterns = [
    path('get_reminders', views.ReminderGetUser.as_view(), name='get_reminders'),
    path('create',  views.ReminderCreate.as_view(), name='create'),
]
