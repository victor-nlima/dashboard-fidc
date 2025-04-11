from django.urls import path
from . import views

urlpatterns = [
    path('dashboard_frame/',views.dashboard_frame,name='dashboard_frame'),
    # path('dashboard_statistics/',views.dashboard_statistics,name='dashboard_statistics'),
    path('created/data/',views.created_data,name='created_data'),
    path('deleted/data/last/',views.delete_last_data,name='delete_data'),
]