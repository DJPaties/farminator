from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.FarmCreate.as_view(), name='create'),
    path('edit/', views.FarmEdit.as_view(), name='create'),
    path('edit/<int:farm_id>/', views.FarmEdit.as_view(), name='get_data'),
    path('delete/', views.FarmDelete.as_view(), name='delete'),
    path('get_all/', views.FarmGetAll.as_view(), name="get_all"),
    path('get_farms/', views.FarmGetUser.as_view(), name="get_farms")
]
