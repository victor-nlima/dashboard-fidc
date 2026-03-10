# views.py for api v1

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from common.models import Fund, FundAccess, CreditStock, TransactionHistory, CashFlow
from .serializers import CreditStockSerializer, TransactionHistorySerializer, CashFlowSerializer
from django.contrib.auth.models import Group
import re

# Utilitário para checar acesso ao fundo

def user_has_fund_access(user, fund):
    if user.is_superuser:
        return True
    user_groups = user.groups.all()
    return FundAccess.objects.filter(fund=fund, group__in=user_groups).exists()

def clean_cnpj(cnpj):
    return re.sub(r'\D', '', cnpj)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_credit_stock(request, cnpj):
    cnpj_clean = clean_cnpj(cnpj)
    try:
        fund = Fund.objects.get(cnpj=cnpj_clean)
    except Fund.DoesNotExist:
        return Response({'detail': 'Fund not found.'}, status=404)
    if not user_has_fund_access(request.user, fund):
        return Response({'detail': 'Access denied.'}, status=403)
    queryset = CreditStock.objects.filter(fund=fund)
    serializer = CreditStockSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_transaction_history(request, cnpj):
    cnpj_clean = clean_cnpj(cnpj)
    try:
        fund = Fund.objects.get(cnpj=cnpj_clean)
    except Fund.DoesNotExist:
        return Response({'detail': 'Fund not found.'}, status=404)
    if not user_has_fund_access(request.user, fund):
        return Response({'detail': 'Access denied.'}, status=403)
    queryset = TransactionHistory.objects.filter(fund=fund)
    serializer = TransactionHistorySerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_cash_flow(request, cnpj):
    cnpj_clean = clean_cnpj(cnpj)
    try:
        fund = Fund.objects.get(cnpj=cnpj_clean)
    except Fund.DoesNotExist:
        return Response({'detail': 'Fund not found.'}, status=404)
    # Check de Instituição
    if not user_has_fund_access(request.user, fund):
        return Response({'detail': 'Access denied.'}, status=403)
    # Check de Setor
    if not request.user.is_superuser and not request.user.has_perm('common.view_cashflow'):
        return Response({'detail': 'Permission denied for CashFlow.'}, status=403)
    queryset = CashFlow.objects.filter(fund=fund)
    serializer = CashFlowSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_credit_stock(request):
    if not request.user.is_superuser:
        return Response({'detail': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)

    fidc_cnpj = request.data.get('fidc_cnpj')
    ref_date = request.data.get('ref_date')
    data = request.data.get('data')

    if not fidc_cnpj or not ref_date or data is None:
        return Response({'detail': 'Campos obrigatórios faltando.'}, status=status.HTTP_400_BAD_REQUEST)

    cnpj_clean = clean_cnpj(fidc_cnpj)
    try:
        fund = Fund.objects.get(cnpj=cnpj_clean)
    except Fund.DoesNotExist:
        return Response({'detail': 'Fundo não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    credit_stock = CreditStock.objects.create(
        fund=fund,
        ref_date=ref_date,
        data=data
    )
    serializer = CreditStockSerializer(credit_stock)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
