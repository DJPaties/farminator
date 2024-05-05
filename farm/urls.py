from django.urls import path
from . import views


urlpatterns = [
    path('create', views.FarmCreate.as_view(), name='create'),
    path('get_all', views.FarmGetAll.as_view(), name="get_all")
]
