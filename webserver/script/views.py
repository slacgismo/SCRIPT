from django.shortcuts import render
from rest_framework import views, viewsets, permissions, mixins, generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from django.http import HttpResponse, JsonResponse
from script.models.data import County
from script.models.statistics import Energy
from script.models.algorithms import Forecast
from script.serializers import CountySerializer, EnergySerializer, ForecastSerializer


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
    filter_fields = ('county', 'year', 'month') # using django-filter


class ForecastViewSet(viewsets.ModelViewSet):
    queryset = Forecast.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = ForecastSerializer
    filter_fields = ('county',) # using django-filter
