from script.models import AlgorithmA
from rest_framework import viewsets, permissions
from .serializers import AlgorithmASerializer

class AlgorithmAViewSet(viewsets.ModelViewSet):
    queryset = AlgorithmA.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = AlgorithmASerializer
