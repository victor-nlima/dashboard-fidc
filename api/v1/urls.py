# urls.py for api v1
from django.urls import path
from .views import TestAPIView

urlpatterns = [
    path('teste/', TestAPIView.as_view(), name='api_v1_teste'),
]
