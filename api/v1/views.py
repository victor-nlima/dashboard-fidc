# views.py for api v1

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from common.models import PositionHistory
from .serializers import PositionHistorySerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_position(request):
    if not request.user.is_superuser:
        return Response({'detail': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = PositionHistorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_positions(request):
    date = request.GET.get('date')
    if request.user.is_superuser:
        queryset = PositionHistory.objects.all()
    else:
        queryset = PositionHistory.objects.filter(group__in=request.user.groups.all())
    if date:
        queryset = queryset.filter(ref_date=date)
    queryset = queryset.order_by('-creation_date').first()
    serializer = PositionHistorySerializer(queryset)
    return Response(serializer.data)
