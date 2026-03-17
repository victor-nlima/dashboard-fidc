from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls'), name='login'),
    path('', include('panel.urls'), name='panel'),
    path('api/v1/', include('api.v1.urls')),
]
