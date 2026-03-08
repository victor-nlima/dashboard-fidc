# serializers.py for api v1

from rest_framework import serializers
from common.models import PositionHistory

class ExampleSerializer(serializers.Serializer):
    message = serializers.CharField()

class PositionHistorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = PositionHistory
        fields = ['id', 'user', 'creation_date', 'ref_date', 'data']
