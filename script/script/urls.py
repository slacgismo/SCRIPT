from rest_framework import routers
from .api import AlgorithmAViewSet

# set up a router for RESTful API
# ref1: https://www.django-rest-framework.org/api-guide/routers/
# ref2: https://www.django-rest-framework.org/api-guide/filtering/
# an idea: /api/<algorithm_name>/<unique_hash_of_parameter>, if algorithm parameters are not too many

router = routers.DefaultRouter()
router.register('api/algorithm_a', AlgorithmAViewSet, 'algorithm_a')

urlpatterns = router.urls
