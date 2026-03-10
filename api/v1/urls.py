# urls.py for api v1
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_position, name='api_create_position'),
    path('list/', views.list_positions, name='api_list_positions'),
]
