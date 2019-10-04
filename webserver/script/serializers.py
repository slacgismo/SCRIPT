from rest_framework import serializers
from script.models import County, Energy, ChargingStation

# serializer of result model

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'


class EnergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Energy
        fields = '__all__'

class ChargingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingStation
        fields = '__all__'
