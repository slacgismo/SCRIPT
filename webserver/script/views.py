from django.shortcuts import render
from rest_framework import views, viewsets, permissions, mixins, generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from django.http import HttpResponse, JsonResponse
from script.models.data import County, ZipCode
from script.models.statistics import Energy
from script.models.algorithms import LoadController, LoadForecast, LoadProfile, GasConsumption, CostBenefit, NetPresentValue, Emission
from script.serializers import CountySerializer, ZipCodeSerializer, EnergySerializer, LoadControllerSerializer, LoadForecastSerializer, LoadProfileSerializer, GasConsumptionSerializer, CostBenefitSerializer, NetPresentValueSerializer, EmissionSerializer


class CountyViewSet(viewsets.ModelViewSet):
    queryset = County.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = CountySerializer


class ZipCodeViewSet(viewsets.ModelViewSet):
    queryset = ZipCode.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = ZipCodeSerializer
    filter_fields = ('county',) # using django-filter


class EnergyViewSet(viewsets.ModelViewSet):
    queryset = Energy.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = EnergySerializer
    filter_fields = ('county', 'year', 'month') # using django-filter


class LoadControllerViewSet(viewsets.ModelViewSet):
    queryset = LoadController.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = LoadControllerSerializer
    filter_fields = ('county',
                    'rate_energy_peak',
                    'rate_energy_partpeak',
                    'rate_energy_offpeak',
                    'rate_demand_peak',
                    'rate_demand_partpeak',
                    'rate_demand_overall') # using django-filter


class LoadForecastViewSet(viewsets.ModelViewSet):
    queryset = LoadForecast.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = LoadForecastSerializer
    filter_fields = ('aggregation_level',
                    'num_evs',
                    'choice',
                    'fast_percent',
                    'work_percent',
                    'res_percent',
                    'l1_percent',
                    'public_l2_percent') # using django-filter


class LoadProfileViewSet(viewsets.ModelViewSet):
    queryset = LoadProfile.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = LoadProfileSerializer
    filter_fields = ('poi',
                    'year',
                    'day_type') # using django-filter


class GasConsumptionViewSet(viewsets.ModelViewSet):
    queryset = GasConsumption.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = GasConsumptionSerializer
    filter_fields = ('year',) # using django-filter


class CostBenefitViewSet(viewsets.ModelViewSet):
    queryset = CostBenefit.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = CostBenefitSerializer
    filter_fields = ('year',) # using django-filter


class NetPresentValueViewSet(viewsets.ModelViewSet):
    queryset = NetPresentValue.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = NetPresentValueSerializer
    filter_fields = ('year',) # using django-filter


class EmissionViewSet(viewsets.ModelViewSet):
    queryset = Emission.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = EmissionSerializer
    filter_fields = ('year',) # using django-filter
