from rest_framework import serializers
from script.models.data import County
from script.models.statistics import Energy
from script.models.algorithms import LoadController

import datetime

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'


class EnergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Energy
        fields = '__all__'


class LoadControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadController
        fields = '__all__'
