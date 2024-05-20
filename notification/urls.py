from django.urls import path
from . import views


urlpatterns = [
    path('get_notifications', views.NotificationGetUser.as_view(), name='get_notification'),
    path('notifyCondition/', views.CheckNotify.as_view(), name='notifyCondition'),
    path('create', views.NotificationCreate.as_view(), name='create'),
]
