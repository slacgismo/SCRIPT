from rest_framework import routers
from .api import CountyViewSet, EnergyViewSet, ChargingStationViewSet

# set up a router for RESTful API
# ref1: https://www.django-rest-framework.org/api-guide/routers/
# ref2: https://www.django-rest-framework.org/api-guide/filtering/
# an idea: /api/<algorithm_name>/<unique_hash_of_parameter>, if algorithm parameters are not too many

# Tip:
# 1. replace space with %20 in the request urls

router = routers.DefaultRouter()
router.register('api/county', CountyViewSet, 'county')
router.register('api/energy', EnergyViewSet, 'energy')
router.register('api/charging_station', ChargingStationViewSet, 'charging_station')

urlpatterns = router.urls

