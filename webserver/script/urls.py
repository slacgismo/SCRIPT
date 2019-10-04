from django.urls import path, include
from rest_framework import routers
from script.views import CountyViewSet, EnergyViewSet, EnergyView

# set up a router for RESTful API
# ref1: https://www.django-rest-framework.org/api-guide/routers/
# ref2: https://www.django-rest-framework.org/api-guide/filtering/
# an idea: /api/<algorithm_name>/<unique_hash_of_parameter>, if algorithm parameters are not too many
# router.register('api/energy/county/(?P<county>[-\w]+)/year/(?P<year>[-\w]+)/month/(?P<month>[-\w]+)', EnergyView.as_view(), 'energy')

# Tip:
# 1. replace space with %20 in the request urls

router = routers.DefaultRouter()
router.register('county', CountyViewSet, 'county')
router.register('energy', EnergyViewSet, 'energy')

urlpatterns = [
    path('debug/', include(router.urls)),
    path('api/energy', EnergyView.as_view()),
]

