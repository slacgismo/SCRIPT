from django.db import models

# Create your models here.

class County(models.Model):
    """County Info"""
    name = models.CharField(max_length=50, primary_key=True)
    residents = models.IntegerField()
    # [TODO] add other basic statistics of the county


class Energy(models.Model):
    """Energy consumed by county and year-month"""
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    energy = models.FloatField()

    class Meta:
        unique_together = (('county', 'year', 'month'),)


class ChargingStation(models.Model):
    """Charging station by county and year-month"""
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    number = models.IntegerField()

    class Meta:
        unique_together = (('county', 'year', 'month'),)
