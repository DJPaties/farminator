from django.urls import path
from . import views


urlpatterns = [
    path('get_notifications', views.NotificationGetUser.as_view(), name='get_notification'),
    path('create', views.NotificationCreate.as_view(), name='create'),
]
