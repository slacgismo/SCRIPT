from django.db import models
from script.models.data import County

class Energy(models.Model):
    """Energy consumed by county and year-month"""
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    energy = models.FloatField()

    class Meta:
        db_table = 'script_energy'
        unique_together = (('county', 'year', 'month'),)

# [TODO] add more statistics
