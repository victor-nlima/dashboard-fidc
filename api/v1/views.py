# views.py for api v1

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ExampleView(APIView):
    def get(self, request):
        return Response({"message": "Hello from API v1"})

class TestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = getattr(request.user, 'username', None)
        return Response({
            "status": "API v1 operando",
            "user": username
        })
