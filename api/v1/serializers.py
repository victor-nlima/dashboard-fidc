from rest_framework import serializers
from common.models import CreditStock, TransactionHistory, CashFlow

class CreditStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditStock
        fields = '__all__'

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = '__all__'

class CashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = '__all__'