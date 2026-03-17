
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import MyTokenObtainPairView

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout_views, name='logout'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]