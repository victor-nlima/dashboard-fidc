from common.models import FundLiability
from datetime import datetime
import os
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from common.models import Fund, CreditStock, TransactionHistory, CashFlow
from .serializers import CreditStockSerializer, TransactionHistorySerializer, CashFlowSerializer, FundLiabilitySerializer
from django.contrib.auth.models import Group
from api.utils.clean_cnpj import clean_cnpj
from api.utils.user_has_fund_access import user_has_fund_access
from api.utils.date_validator import date_validator
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.conf import settings

logger = logging.getLogger('api_logger')

# Parâmetro reutilizável para a Doc
DATE_REF_PARAM = OpenApiParameter(
    name='date_ref', 
    description='Data de referência (YYYY-MM-DD)', 
    required=False, 
    type=OpenApiTypes.DATE,
    location=OpenApiParameter.QUERY
)

# List FundLiability
@extend_schema(parameters=[OpenApiParameter(
    name='cnpj',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.PATH,
    description='CNPJ do fundo (somente números).',
    pattern=r'^\d{14}$',
), DATE_REF_PARAM], responses={200: FundLiabilitySerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_fund_liability(request, cnpj):
    cnpj_clean = clean_cnpj(cnpj)
    ref_date = request.query_params.get('ref_date')
    try:
        fund = Fund.objects.get(cnpj=cnpj_clean)
    except Fund.DoesNotExist:
        return Response({'detail': 'Fund not found.'}, status=404)
    if not user_has_fund_access(request.user, fund):
        return Response({'detail': 'Access denied.'}, status=403)
    if not request.user.is_superuser and not request.user.has_perm('common.view_fundliability'):
        return Response({'detail': 'Permission denied for FundLiability.'}, status=403)
    queryset = FundLiability.objects.filter(fund=fund)
    if ref_date:
        ref_date = date_validator(ref_date)
        if isinstance(ref_date, Response):
            return ref_date
        try:
            queryset = queryset.filter(ref_date=ref_date).order_by('-created_at').first()
            serializer = FundLiabilitySerializer(queryset)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': 'Data de referência inválida.'}, status=400)
    serializer = FundLiabilitySerializer(queryset, many=True)
    return Response(serializer.data)

# Create FundLiability
@extend_schema(exclude=True)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_fund_liability(request):
    if not request.user.is_superuser:
        return Response({'detail': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)

    cnpj = request.data.get('fidc_cnpj')
    ref_date = request.data.get('ref_date')
    data = request.data.get('data')

    if not cnpj or not ref_date or data is None:
        return Response({'detail': 'Campos obrigatórios faltando.'}, status=status.HTTP_400_BAD_REQUEST)

    cnpj_clean = clean_cnpj(cnpj)
    try:
        fund = Fund.objects.get(cnpj=cnpj_clean)
    except Fund.DoesNotExist:
        return Response({'detail': 'Fundo não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        logger.exception('Erro ao buscar fundo em create_fund_liability')
        return Response({'detail': 'Erro interno ao processar a requisição.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Limite de registros: 15
    qs = FundLiability.objects.filter(fund=fund, ref_date=ref_date).order_by('created_at')
    if qs.count() >= 15:
        to_delete = qs[:qs.count() - 14]
        for obj in to_delete:
            obj.delete()

    fund_liability = FundLiability.objects.create(
        fund=fund,
        ref_date=ref_date,
        data=data
    )
    serializer = FundLiabilitySerializer(fund_liability)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
# views.py for api v1

@extend_schema(parameters=[OpenApiParameter(
            name='cnpj',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description='CNPJ do fundo (somente números).',
            pattern=r'^\d{14}$',
        ),DATE_REF_PARAM], responses={200: CreditStockSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_credit_stock(request, cnpj):
    cnpj_clean = clean_cnpj(cnpj)
    ref_date = request.query_params.get('ref_date')

    try:
        fund = Fund.objects.get(cnpj=cnpj_clean)
    except Fund.DoesNotExist:
        return Response({'detail': 'Fund not found.'}, status=404)
    if not user_has_fund_access(request.user, fund):
        return Response({'detail': 'Access denied.'}, status=403)
    if not request.user.is_superuser and not request.user.has_perm('common.view_creditstock'):
        return Response({'detail': 'Permission denied for CreditStock.'}, status=403)
    queryset = CreditStock.objects.filter(fund=fund)

    if ref_date:
        ref_date = date_validator(ref_date)
        if isinstance(ref_date, Response):
            return ref_date
        try:
            queryset = queryset.filter(ref_date=ref_date).order_by('-created_at').first()
            serializer = CreditStockSerializer(queryset)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': 'Data de referência inválida.'}, status=400)
    
    serializer = CreditStockSerializer(queryset, many=True)
    return Response(serializer.data)

@extend_schema(parameters=[OpenApiParameter(
            name='cnpj',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description='CNPJ do fundo (somente números).',
            pattern=r'^\d{14}$',
        ),DATE_REF_PARAM], responses={200: TransactionHistorySerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_transaction_history(request, cnpj):
    ref_date = request.query_params.get('ref_date')
    cnpj_clean = clean_cnpj(cnpj)
    
    try:
        fund = Fund.objects.get(cnpj=cnpj_clean)
    except Fund.DoesNotExist:
        return Response({'detail': 'Fund not found.'}, status=404)
    if not user_has_fund_access(request.user, fund):
        return Response({'detail': 'Access denied.'}, status=403)
    if not request.user.is_superuser and not request.user.has_perm('common.view_transactionhistory'):
        return Response({'detail': 'Permission denied for TransactionHistory.'}, status=403)
    queryset = TransactionHistory.objects.filter(fund=fund)

    if ref_date:
        ref_date = date_validator(ref_date)
        
        if isinstance(ref_date, Response):
            return ref_date
        
        try:
            queryset = queryset.filter(ref_date=ref_date).order_by('-created_at').first()
            serializer = TransactionHistorySerializer(queryset)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': 'Data de referência inválida.'}, status=400)

    serializer = TransactionHistorySerializer(queryset, many=True)
    return Response(serializer.data)

@extend_schema(parameters=[OpenApiParameter(
            name='cnpj',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description='CNPJ do fundo (somente números).',
            pattern=r'^\d{14}$',
        ),DATE_REF_PARAM], responses={200: CashFlowSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_cash_flow(request, cnpj):
    cnpj_clean = clean_cnpj(cnpj)
    date_ref = request.query_params.get('ref_date')

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
    if date_ref:
        date_ref = date_validator(date_ref)
        
        if isinstance(date_ref, Response):
            return date_ref
        
        try:
            queryset = queryset.filter(ref_date=date_ref).order_by('-created_at').first()
            serializer = CashFlowSerializer(queryset)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': 'Data de referência inválida.'}, status=400)
    serializer = CashFlowSerializer(queryset, many=True)
    return Response(serializer.data)

@extend_schema(exclude=True)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_credit_stock(request):
    if not request.user.is_superuser:
        return Response({'detail': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)

    cnpj = request.data.get('fidc_cnpj')
    ref_date = request.data.get('ref_date')
    data = request.data.get('data')

    if not cnpj or not ref_date or data is None:
        return Response({'detail': 'Campos obrigatórios faltando.'}, status=status.HTTP_400_BAD_REQUEST)

    cnpj_clean = clean_cnpj(cnpj)
    try:
        fund = Fund.objects.get(cnpj=cnpj_clean)
    except Fund.DoesNotExist:
        return Response({'detail': 'Fundo não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        logger.exception('Erro ao buscar fundo em create_credit_stock')
        return Response({'detail': 'Erro interno ao processar a requisição.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Limite de registros: 15
    qs = CreditStock.objects.filter(fund=fund, ref_date=ref_date).order_by('created_at')
    if qs.count() >= 15:
        to_delete = qs[:qs.count() - 14]
        for obj in to_delete:
            obj.delete()

    credit_stock = CreditStock.objects.create(
        fund=fund,
        ref_date=ref_date,
        data=data
    )
    serializer = CreditStockSerializer(credit_stock)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(exclude=True)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_cash_flow(request):
    # Trava de segurança: Só o Root (Superuser) entra
    if not request.user.is_superuser:
        return Response({"detail": "Permission denied. Only root can upload data."}, status=403)

    cnpj = request.data.get('fidc_cnpj')
    ref_date = request.data.get('ref_date')
    json_data = request.data.get('data')
    cnpj_clean = clean_cnpj(cnpj)
    try:
        # Busca o fundo pelo CNPJ para garantir que o dado tem dono
        fund = Fund.objects.get(cnpj=cnpj_clean)
    except Fund.DoesNotExist:
        return Response({"detail": f"Fund with CNPJ {cnpj} not found."}, status=404)
    except Exception:
        logger.exception('Erro ao buscar fundo em create_cash_flow')
        return Response({'detail': 'Erro interno ao processar a requisição.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Limite de registros: 15
    qs = CashFlow.objects.filter(fund=fund, ref_date=ref_date).order_by('created_at')
    if qs.count() >= 15:
        to_delete = qs[:qs.count() - 14]
        for obj in to_delete:
            obj.delete()

    cash_record = CashFlow.objects.create(
        fund=fund,
        ref_date=ref_date,
        data=json_data
    )

    return Response({
        "detail": "Cash Flow uploaded successfully", 
        "id": cash_record.id
    }, status=201)

@extend_schema(exclude=True)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction_history(request):
    if not request.user.is_superuser:
        return Response({"detail": "Permission denied. Only root can upload data."}, status=403)

    cnpj = request.data.get('fidc_cnpj')
    ref_date = request.data.get('ref_date')
    json_data = request.data.get('data')
    cnpj_clean = clean_cnpj(cnpj)
    try:
        fund = Fund.objects.get(cnpj=cnpj_clean)
    except Fund.DoesNotExist:
        return Response({"detail": f"Fund with CNPJ {cnpj} not found."}, status=404)
    except Exception:
        logger.exception('Erro ao buscar fundo em create_transaction_history')
        return Response({'detail': 'Erro interno ao processar a requisição.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Limite de registros: 15
    qs = TransactionHistory.objects.filter(fund=fund, ref_date=ref_date).order_by('created_at')
    if qs.count() >= 15:
        to_delete = qs[:qs.count() - 14]
        for obj in to_delete:
            obj.delete()

    transaction_record = TransactionHistory.objects.create(
        fund=fund,
        ref_date=ref_date,
        data=json_data
    )

    return Response({
        "detail": "Transaction History uploaded successfully", 
        "id": transaction_record.id
    }, status=201)

@extend_schema(
    parameters=[
        OpenApiParameter(name='ref_date', description='Data de referência (YYYY-MM-DD)', required=True, type=OpenApiTypes.DATE),
        OpenApiParameter(
            name='cnpj',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description='CNPJ do fundo (somente números).',
            pattern=r'^\d{14}$',
        )
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_consolidated(request, cnpj):
    cnpj_clean = clean_cnpj(cnpj)
    ref_date = request.query_params.get('ref_date')

    if not ref_date:
        return Response({'detail': 'A data de referência (ref_date) é obrigatória.'}, status=400)

    try:
        fund = Fund.objects.get(cnpj=cnpj_clean)
    except Fund.DoesNotExist:
        return Response({'detail': 'Fundo não encontrado.'}, status=404)

    # 1. Check de Instituição
    if not user_has_fund_access(request.user, fund):
        return Response({'detail': 'Acesso negado ao fundo.'}, status=403)

    # Check de Setor para o Caixa
    has_cash_perm = request.user.is_superuser or request.user.has_perm('common.view_cashflow')
    cash = None
    if has_cash_perm:
        cash = CashFlow.objects.filter(fund=fund, ref_date=ref_date).last()

    has_stock_perm = request.user.is_superuser or request.user.has_perm('common.view_creditstock')
    stock = None
    if has_stock_perm:
        stock = CreditStock.objects.filter(fund=fund, ref_date=ref_date).last()
    
    has_transactions_perm = request.user.is_superuser or request.user.has_perm('common.view_transactionhistory')
    transactions = None
    if has_transactions_perm:
        transactions = TransactionHistory.objects.filter(fund=fund, ref_date=ref_date).last()
        
    # Permissão para FundLiability
    has_liability_perm = request.user.is_superuser or request.user.has_perm('common.view_fundliability')
    liability = None
    if has_liability_perm:
        from common.models import FundLiability
        liability = FundLiability.objects.filter(fund=fund, ref_date=ref_date).order_by('-created_at').first()

    context = {
        "nome_fundo": fund.name,
        "cnpj_fundo": fund.cnpj,
        "data_referencia": ref_date,
        "dados": {
            "estoque": CreditStockSerializer(stock).data if stock else ({"detail": "Permission denied"} if not has_stock_perm else None),
            "movimentacoes": TransactionHistorySerializer(transactions).data if transactions else ({"detail": "Permission denied"} if not has_transactions_perm else None),
            "caixa": CashFlowSerializer(cash).data if cash else ({"detail": "Permission denied"} if not has_cash_perm else None),
            "passivo": FundLiabilitySerializer(liability).data if liability else ({"detail": "Permission denied"} if not has_liability_perm else None)
        }
    }

    return Response(context)

@extend_schema(exclude=True)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_system_logs(request):
    log_path = os.path.join(settings.BASE_DIR, 'logs/api_access.log')
    if not os.path.exists(log_path):
        return Response({"detail": "Arquivo de log não encontrado."}, status=404)

    try:
        limit = int(request.query_params.get('limit', 500))
        limit = max(1, min(limit, 2000))
        with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()[-limit:]

        return Response({
            "arquivo": "api_logs.log",
            "total_retornado": len(lines),
            "conteudo": lines
        })
    except Exception:
        logger.exception('Erro ao ler arquivo de log')
        return Response({"detail": "Erro ao ler o arquivo de log."}, status=500)