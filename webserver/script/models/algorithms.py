from django.db import models
from django.contrib.postgres.fields import JSONField
from script.models.data import County

# Create your models of algorithm results here.

class LoadController(models.Model):
    """Algorithm: Load Controller
        inputs: county
        outputs：
            (1) uncontrolled load
            (2) controlled load (cvx optimized)
        visualizations:
            (1) uncontrolled load (load - time)
            (2) controlled load (cvx optimized) (load - time)
    """
    
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    uncontrolled_load = JSONField()
    controlled_load = JSONField()

    class Meta:
        db_table = 'script_algorithm_load_controller'
