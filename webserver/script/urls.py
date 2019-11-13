from django.urls import path, include
from rest_framework import routers
from script.views import CountyViewSet, ZipCodeViewSet, EnergyViewSet, LoadControllerViewSet, LoadProfileViewSet

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

# Algorithm-1: load controller
router.register('algorithm/load_controller', LoadControllerViewSet, 'algorithm/load_controller')

# Algorithm-2: cost benefit analysis
router.register('algorithm/cost_benefit_analysis/load_profile', LoadProfileViewSet, 'algorithm/cost_benefit_analysis/load_profile')

urlpatterns = [
    path('', include(router.urls)),
]
