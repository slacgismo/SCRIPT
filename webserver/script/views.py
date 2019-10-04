from django.shortcuts import render
from rest_framework import views, viewsets, permissions, mixins, generics
from script.models import County, Energy, ChargingStation
from .serializers import CountySerializer, EnergySerializer, ChargingStationSerializer
from rest_framework.response import Response

import json


class CountyViewSet(viewsets.ModelViewSet):
    queryset = County.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = CountySerializer
    # currently POST is allowed just for debugging
    # http_method_names = ['get',]


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


class EnergyView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    queryset = Energy.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = EnergySerializer

    # [TODO] get & validate the params in an additional func

    def get(self, request, *args, **kwargs):
        county_name = request.query_params.get('county', None)
        county = County.objects.get(name=county_name)
        year = request.query_params.get('year', None)
        month = request.query_params.get('month', None)
        res = Energy.objects.get(county=county, year=year, month=month)
        serializer = self.serializer_class(res)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        county_name = request.query_params.get('county', None)
        county = County.objects.get(name=county_name)
        year = request.query_params.get('year', None)
        month = request.query_params.get('month', None)
        energy = request.query_params.get('energy', None)
        res = Energy.objects.get(county=county, year=year, month=month)
        res.energy = energy
        res.save()
        serializer = self.serializer_class(res)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        county_name = request.query_params.get('county', None)
        county = County.objects.get(name=county_name)
        year = request.query_params.get('year', None)
        month = request.query_params.get('month', None)
        energy = request.query_params.get('energy', None)
        res = Energy.objects.create(county=county, year=year, month=month, energy=energy)
        serializer = self.serializer_class(res)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        county_name = request.query_params.get('county', None)
        county = County.objects.get(name=county_name)
        year = request.query_params.get('year', None)
        month = request.query_params.get('month', None)
        res = Energy.objects.get(county=county, year=year, month=month)
        res.delete()
        serializer = self.serializer_class(res)
        return Response(serializer.data)

