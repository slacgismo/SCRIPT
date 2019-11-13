from rest_framework import serializers
from script.models.data import County, ZipCode
from script.models.statistics import Energy
from script.models.algorithms import LoadController, LoadProfile, GasConsumption

import datetime

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'


class ZipCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZipCode
        fields = '__all__'

class EnergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Energy
        fields = '__all__'


class LoadControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadController
        fields = '__all__'


class LoadProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadProfile
        fields = '__all__'


class GasConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasConsumption
        fields = '__all__'
