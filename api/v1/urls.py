# urls.py for api v1
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from . import views

urlpatterns = [
    path('credit-stock/<str:cnpj>/', views.list_credit_stock, name='list_credit_stock'),
    path('transaction-history/<str:cnpj>/', views.list_transaction_history, name='list_transaction_history'),
    path('cash-flow/<str:cnpj>/', views.list_cash_flow, name='list_cash_flow'),
    path('create/credit-stock/', views.create_credit_stock, name='create_credit_stock'),
    path('create/cash-flow/', views.create_cash_flow, name='create_cash_flow'),
    path('create/transaction-history/', views.create_transaction_history, name='create_transaction_history'),
    path('consolidated/<str:cnpj>/', views.get_consolidated, name='consolidated'),
    path('system/logs/', views.get_system_logs, name='logs'),
    path('fund-liability/<str:cnpj>/', views.list_fund_liability, name='list_fund_liability'),
    path('create/fund-liability/', views.create_fund_liability, name='create_fund_liability'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
