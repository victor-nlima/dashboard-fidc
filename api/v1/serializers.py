from rest_framework import serializers
from common.models import CreditStock, TransactionHistory, CashFlow, FundLiability

class BaseFidcSerializer(serializers.ModelSerializer):
    fundo = serializers.SlugRelatedField(
        source='fund', 
        read_only=True, 
        slug_field='cnpj'
    )
    
    data_referencia = serializers.DateField(source='ref_date')
    criado_em = serializers.DateTimeField(source='created_at', format="%d/%m/%Y %H:%M:%S")
    atualizado_em = serializers.DateTimeField(source='updated_at', format="%d/%m/%Y %H:%M:%S")
    class Meta:
        abstract = True

class CreditStockSerializer(BaseFidcSerializer):
    class Meta:
        model = CreditStock
        fields = ['id', 'fundo', 'data', 'data_referencia', 'criado_em', 'atualizado_em']

class TransactionHistorySerializer(BaseFidcSerializer):
    class Meta:
        model = TransactionHistory
        fields = ['id', 'fundo', 'data', 'data_referencia', 'criado_em', 'atualizado_em']

class CashFlowSerializer(BaseFidcSerializer):
    class Meta:
        model = CashFlow
        fields = ['id', 'fundo', 'data', 'data_referencia', 'criado_em', 'atualizado_em']

# FundLiabilitySerializer
class FundLiabilitySerializer(BaseFidcSerializer):
    class Meta:
        model = FundLiability
        fields = ['id', 'fundo', 'data', 'data_referencia', 'criado_em', 'atualizado_em']