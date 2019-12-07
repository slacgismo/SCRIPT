from django.urls import path, include
from rest_framework import routers
from script.views import CountyViewSet, ZipCodeViewSet, EnergyViewSet
from script.views import LoadControllerConfigViewSet, LoadForecastConfigViewSet, LoadProfileConfigViewSet, GasConsumptionConfigViewSet, NetPresentValueConfigViewSet, EmissionConfigViewSet, CostBenefitConfigViewSet
from script.views import LoadForecastViewSet, LoadControllerViewSet, LoadProfileViewSet, GasConsumptionViewSet, CostBenefitViewSet, NetPresentValueViewSet, EmissionViewSet


# set up a router for RESTful API
# ref1: https://www.django-rest-framework.org/api-guide/routers/
# ref2: https://www.django-rest-framework.org/api-guide/filtering/
# an idea: /api/<algorithm_name>/<unique_hash_of_parameter>, if algorithm parameters are not too many
# router.register('api/energy/county/(?P<county>[-\w]+)/year/(?P<year>[-\w]+)/month/(?P<month>[-\w]+)', EnergyView.as_view(), 'energy')

# Tip:
# 1. replace space with %20 in the request urls

router = routers.DefaultRouter()
router.register('county', CountyViewSet, 'county')
router.register('zipcode', ZipCodeViewSet, 'zipcode')
router.register('energy', EnergyViewSet, 'energy')


# Configuration for algorithms:
router.register('config/load_controller', LoadControllerConfigViewSet, 'config/load_controller')
router.register('config/load_forecast', LoadForecastConfigViewSet, 'config/load_forecast')
router.register('config/load_profile', LoadProfileConfigViewSet, 'config/load_profile')
router.register('config/gas_consumption', GasConsumptionConfigViewSet, 'config/gas_consumption')
router.register('config/net_present_value', NetPresentValueConfigViewSet, 'config/net_present_value')
router.register('config/emission', EmissionConfigViewSet, 'config/emission')
router.register('config/cost_benefit', CostBenefitConfigViewSet, 'config/cost_benefit')


# Algorithm-1: load controller
router.register('algorithm/load_controller', LoadControllerViewSet, 'algorithm/load_controller')

# Algorithm-2: EV load forecast
router.register('algorithm/load_forecast', LoadForecastViewSet, 'algorithm/load_forecast')

# Algorithm-3: cost benefit analysis
router.register('algorithm/cost_benefit_analysis/load_profile', LoadProfileViewSet, 'algorithm/cost_benefit_analysis/load_profile')
router.register('algorithm/cost_benefit_analysis/gas_consumption', GasConsumptionViewSet, 'algorithm/cost_benefit_analysis/gas_consumption')
router.register('algorithm/cost_benefit_analysis/cost_benefit', CostBenefitViewSet, 'algorithm/cost_benefit_analysis/cost_benefit')
router.register('algorithm/cost_benefit_analysis/net_present_value', NetPresentValueViewSet, 'algorithm/cost_benefit_analysis/net_present_value')
router.register('algorithm/cost_benefit_analysis/emission', EmissionViewSet, 'algorithm/cost_benefit_analysis/emission')


urlpatterns = [
    path('', include(router.urls)),
]
