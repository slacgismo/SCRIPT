from rest_framework import serializers
from script.models.data import County
from script.models.statistics import Energy
from script.models.algorithms import Forecast

import datetime

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'

    def validate_residents(self, residents):
        if residents < 0:
            raise serializers.ValidationError("Residents must be a positive.")
        return residents


class EnergySerializer(serializers.ModelSerializer):

    def validate_year(self, year):
        if year < 2000 or year > datetime.datetime.now().year:
            raise serializers.ValidationError("Year must be 2000~now.")
        return year
    
    def validate_month(self, month):
        if month < 1 or month > 12:
            raise serializers.ValidationError("Month must be 1~12.")
        return month

    class Meta:
        model = Energy
        fields = '__all__'


class ForecastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forecast
        fields = '__all__'
