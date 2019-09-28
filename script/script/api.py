from rest_framework import viewsets, permissions
from script.models import County, Energy, ChargingStation
from .serializers import CountySerializer, EnergySerializer, ChargingStationSerializer

class CountyViewSet(viewsets.ModelViewSet):
    queryset = County.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = CountySerializer


class EnergyViewSet(viewsets.ModelViewSet):
    queryset = Energy.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = EnergySerializer


class ChargingStationViewSet(viewsets.ModelViewSet):
    queryset = ChargingStation.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = ChargingStationSerializer
