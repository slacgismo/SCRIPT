from django.shortcuts import render
from rest_framework import views, viewsets, permissions, mixins, generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.http import HttpResponse, JsonResponse
import json

from script.models.data import County, ZipCode
from script.models.statistics import Energy
from script.models.config import LoadControllerConfig, LoadForecastConfig, GasConsumptionConfig, CostBenefitConfig, EmissionConfig
from script.models.algorithms import LoadController, LoadForecast, GasConsumption, CostBenefit, Emission
from script.serializers import LoadControllerConfigSerializer, LoadForecastConfigSerializer, EmissionConfigSerializer, CostBenefitConfigSerializer, GasConsumptionConfigSerializer
from script.serializers import CountySerializer, ZipCodeSerializer, EnergySerializer
from script.serializers import LoadControllerSerializer, LoadForecastSerializer, GasConsumptionSerializer, CostBenefitSerializer, EmissionSerializer
from script.SmartCharging.SmartChargingAlgorithm import *
from script.SmartCharging.SmartChargingDefault import getScaData
from script.tasks import run_cba_tool, run_lf_runner

class LoadControlRunner(APIView):
    def post(self, request, format=None):
        ''' currently only runs with default data '''
        item_controlled = request.data["county"] + "_controlled_" + request.data["rateStructure"] + "_200_outputs.npy"
        item_uncontrolled = request.data["county"] + "_uncontrolled_200_inputs.npy"
        sca_response = {"controlled_load" : getScaData(item_controlled), "uncontrolled_load" : getScaData(item_uncontrolled)}
        return Response(json.dumps(sca_response))

class CostBenefitAnalysisRunner(APIView):
    def post(self, request, format=None):
        task = run_cba_tool.delay(request.data["load_profile"], request.data["county"])
        cba_response = {"task_id": task.id, "status": task.status}
        return Response(cba_response)

class LoadForecastRunner(APIView):
    def post(self, request, format=None):
        for key, item in request.data.items():
            if item in ["None", "none", "NONE"]:
                request.data[key] = None

        lf_argv = {
            "total_num_evs": request.data["numEvs"],
            "aggregation_level": request.data["aggregationLevel"],
            "county": request.data["county"],
            "fast_percent": request.data["fastPercent"],
            "work_percent": request.data["workPercent"],
            "res_percent": request.data["resPercent"],
            "l1_percent": request.data["l1Percent"],
            "publicl2_percent": request.data["publicL2Percent"],
            "res_daily_use": request.data["resDailyUse"],
            "work_daily_use": request.data["workDailyUse"],
            "fast_daily_use": request.data["fastDailyUse"],
            "rent_percent": request.data["rentPercent"],
            "res_l2_smooth": request.data["resL2Smooth"],
            "week_day": request.data["weekDay"],
            "publicl2_daily_use": request.data["publicL2DailyUse"],
            "small_batt": request.data["smallBatt"],
            "big_batt": request.data["bigBatt"],
            "all_batt": request.data["allBatt"],
            "timer_control": request.data["timerControl"],
            "work_control": request.data["workControl"],
            "config_name": request.data["configName"]
        }
        
        task = run_lf_runner.delay(lf_argv)
        lf_response = {"task_id": task.id, "status": task.status}

        return Response(lf_response)

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



class LoadControllerConfigViewSet(viewsets.ModelViewSet):
    queryset = LoadControllerConfig.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = LoadControllerConfigSerializer
    filter_fields = ('county',
                    'rate_energy_peak',
                    'rate_energy_partpeak',
                    'rate_energy_offpeak',
                    'rate_demand_peak',
                    'rate_demand_partpeak',
                    'rate_demand_overall') # using django-filter


class LoadForecastConfigViewSet(viewsets.ModelViewSet):
    queryset = LoadForecastConfig.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = LoadForecastConfigSerializer
    filter_fields = ('config_name',
                    'aggregation_level',
                    'num_evs',
                    'choice',
                    'fast_percent',
                    'work_percent',
                    'res_percent',
                    'l1_percent',
                    'public_l2_percent') # using django-filter


# class LoadProfileConfigViewSet(viewsets.ModelViewSet):
#     queryset = LoadProfileConfig.objects.all()
#     permission_classes = [
#         permissions.AllowAny,
#     ]
#     serializer_class = LoadProfileConfigSerializer
#     filter_fields = ('lf_config',
#                     'poi',
#                     'year',
#                     'day_type') # using django-filter


class GasConsumptionConfigViewSet(viewsets.ModelViewSet):
    queryset = GasConsumptionConfig.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = GasConsumptionConfigSerializer
    filter_fields = ('lf_config',
                    'year') # using django-filter


# class NetPresentValueConfigViewSet(viewsets.ModelViewSet):
#     queryset = NetPresentValueConfig.objects.all()
#     permission_classes = [
#         permissions.AllowAny,
#     ]
#     serializer_class = NetPresentValueConfigSerializer
#     filter_fields = ('lf_config',
#                     'year') # using django-filter


class EmissionConfigViewSet(viewsets.ModelViewSet):
    queryset = EmissionConfig.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = EmissionConfigSerializer
    filter_fields = ('lf_config',
                    'year') # using django-filter


class CostBenefitConfigViewSet(viewsets.ModelViewSet):
    queryset = CostBenefitConfig.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = CostBenefitConfigSerializer
    filter_fields = ('lf_config',
                    'year') # using django-filter


class LoadControllerViewSet(viewsets.ModelViewSet):
    queryset = LoadController.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = LoadControllerSerializer
    filter_fields = ('config',) # using django-filter


class LoadForecastViewSet(viewsets.ModelViewSet):
    queryset = LoadForecast.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = LoadForecastSerializer
    filter_fields = ('config',) # using django-filter


# class LoadProfileViewSet(viewsets.ModelViewSet):
#     queryset = LoadProfile.objects.all()
#     permission_classes = [
#         permissions.AllowAny,
#     ]
#     serializer_class = LoadProfileSerializer
#     filter_fields = ('config',) # using django-filter


class GasConsumptionViewSet(viewsets.ModelViewSet):
    queryset = GasConsumption.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = GasConsumptionSerializer
    filter_fields = ('config',) # using django-filter


class CostBenefitViewSet(viewsets.ModelViewSet):
    queryset = CostBenefit.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = CostBenefitSerializer
    filter_fields = ('config',) # using django-filter


# class NetPresentValueViewSet(viewsets.ModelViewSet):
#     queryset = NetPresentValue.objects.all()
#     permission_classes = [
#         permissions.AllowAny,
#     ]
#     serializer_class = NetPresentValueSerializer
#     filter_fields = ('config',) # using django-filter


class EmissionViewSet(viewsets.ModelViewSet):
    queryset = Emission.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = EmissionSerializer
    filter_fields = ('config',) # using django-filter
