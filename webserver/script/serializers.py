from rest_framework import serializers
from script.models.data import County, ZipCode
from script.models.statistics import Energy
from script.models.config import LoadControllerConfig, LoadForecastConfig, LoadProfileConfig, GasConsumptionConfig, CostBenefitConfig, NetPresentValueConfig, EmissionConfig
from script.models.algorithms import LoadController, LoadForecast, LoadProfile, GasConsumption, CostBenefit, NetPresentValue, Emission

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


class LoadControllerConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadControllerConfig
        fields = '__all__'


class LoadForecastConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadForecastConfig
        fields = '__all__'


class LoadProfileConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadProfileConfig
        fields = '__all__'


class EmissionConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionConfig
        fields = '__all__'


class NetPresentValueConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetPresentValueConfig
        fields = '__all__'


class CostBenefitConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostBenefitConfig
        fields = '__all__'


class GasConsumptionConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasConsumptionConfig
        fields = '__all__'


class LoadControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadController
        fields = '__all__'


class LoadForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadForecast
        fields = '__all__'


class LoadProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadProfile
        fields = '__all__'
        depth = 1

class GasConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasConsumption
        fields = '__all__'
        depth = 1


class CostBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostBenefit
        fields = '__all__'
        depth = 1

class NetPresentValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetPresentValue
        fields = '__all__'
        depth = 1

class EmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emission
        fields = '__all__'
        depth = 1
