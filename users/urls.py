from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('',views.logout_views,name='logout')
]