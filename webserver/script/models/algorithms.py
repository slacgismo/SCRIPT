from django.db import models
from django.contrib.postgres.fields import JSONField
from script.models.data import County
from script.models.enums import DayType, POI
from script.validators import validate_positive, validate_year

# Create your models of algorithm results here.

class LoadController(models.Model):
    """Algorithm: Load Controller
        inputs:
            (1) county
            (2) rate_energy_peak
            (3) rate_energy_partpeak
            (4) rate_energy_offpeak
            (5) rate_demand_peak
            (6) rate_demand_partpeak
            (7) rate_demand_overall
        outputs：
            (1) uncontrolled load
            (2) controlled load (cvx optimized)
        visualizations:
            (1) uncontrolled load (load - time)
            (2) controlled load (cvx optimized) (load - time)
    """
    
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    rate_energy_peak = models.FloatField(validators=[validate_positive])
    rate_energy_partpeak = models.FloatField(validators=[validate_positive])
    rate_energy_offpeak = models.FloatField(validators=[validate_positive])
    rate_demand_peak = models.FloatField(validators=[validate_positive])
    rate_demand_partpeak = models.FloatField(validators=[validate_positive])
    rate_demand_overall = models.FloatField(validators=[validate_positive])
    uncontrolled_load = JSONField()
    controlled_load = JSONField()

    class Meta:
        db_table = 'script_algorithm_load_controller'
        unique_together = (('county',
                            'rate_energy_peak',
                            'rate_energy_partpeak',
                            'rate_energy_offpeak',
                            'rate_demand_peak',
                            'rate_demand_partpeak',
                            'rate_demand_overall'),)    


class LoadProfile(models.Model):
    """Algorithm: Cost Benefit Analysis of Load Profile including
            Aggregate Load Profile,
            DCFC Load Profile, 
            Residential Load Profile,
            Public L2 Load Profile,
            Workplace Load Profile.
        inputs:
            TODO
        outputs:
            (1) load profile throughout 24 hours of a weekday
            (2) load profile throughout 24 hours of a weekend
        visualizations:
            TODO @Yanqing @Xinyi
    """

    poi = models.CharField(max_length=20, choices=POI.choices(), default=POI.UNKNOWN)
    year = models.IntegerField()
    day_type = models.CharField(max_length=10, choices=DayType.choices(), default=DayType.WEEKDAY)
    loads = JSONField()

    class Meta:
        db_table = 'script_algorithm_cba_load_profile'
        unique_together = (('poi', 'year', 'day_type'),)


class GasConsumption(models.Model):
    """Algorithm: Cost Benefit Analysis of Annual Gas Consumption including
            Gasoline Consumption (gallons)
            Gasoline Consumption (MMBTU)
            Gasoline Emissions (metric tons CO2)
            PHEV 10 Gasoline Consumption (gallons)
            PHEV 10 Gasoline Consumption (MMBTU)
            PHEV 10 Gasoline Emissions (metric tons CO2)
            PHEV 20 Gasoline Consumption (gallons)
            PHEV 20 Gasoline Consumption (MMBTU)
            PHEV 20 Gasoline Emissions (metric tons CO2)
            PHEV 40 Gasoline Consumption (gallons)
            PHEV 40 Gasoline Consumption (MMBTU)
            PHEV 40 Gasoline Emissions (metric tons CO2)
            BEV 100 Gasoline Consumption (gallons)
            BEV 100 Gasoline Consumption (MMBTU)
            BEV 100 Gasoline Emissions (metric tons CO2)
            EEV Share (%)
        inputs:
            TODO
        outputs:
            (1) gasoline consumption/emissions in the next several decades, as well as EV share
        visualizations:
            TODO @Yanqing @Xinyi
    """

    year = models.IntegerField()
    consumption = JSONField()

    class Meta:
        db_table = 'script_algorithm_cba_gas_consumption'
        unique_together = (('year',),)
