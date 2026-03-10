from rest_framework import serializers
from common.models import PositionHistory

# Serializer básico para PositionHistory, incluindo todos os campos do model
class PositionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionHistory
        fields = '__all__'