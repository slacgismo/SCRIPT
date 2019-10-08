from django.db import models
from django.contrib.postgres.fields import JSONField
from script.models.data import County

# Create your models of algorithm results here.

class Forecast(models.Model):
    """Algorithm: Forecast"""
    # inputs: county, ... [TODO]
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    # outputs: JSON: energy-time
    results = JSONField()

    class Meta:
        db_table = 'script_algorithm_forecast'
