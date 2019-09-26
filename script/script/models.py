from django.db import models

# Create your models here.
class AlgorithmA(models.Model):
    algorithm_name = models.CharField(max_length=100)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
