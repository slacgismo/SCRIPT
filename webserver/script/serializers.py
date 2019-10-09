from rest_framework import serializers
from script.models.data import County
from script.models.statistics import Energy

import datetime

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'


class EnergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Energy
        fields = '__all__'
