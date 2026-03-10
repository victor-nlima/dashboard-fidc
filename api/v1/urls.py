# urls.py for api v1
from django.urls import path
from . import views

urlpatterns = [
    path('credit-stock/<str:cnpj>/', views.list_credit_stock, name='list_credit_stock'),
    path('transaction-history/<str:cnpj>/', views.list_transaction_history, name='list_transaction_history'),
    path('cash-flow/<str:cnpj>/', views.list_cash_flow, name='list_cash_flow'),
    path('credit-stock/create/', views.create_credit_stock, name='create_credit_stock'),
]
