from django.db import models
from script.models.data import County
from script.models.enums import DayType, POI, AggregationLevel
# Create your models of config of algorithm results here.

class LoadControllerConfig(models.Model):
    """Algorithm: Load Controller inputs:
        (1) county
        (2) rate_energy_peak
        (3) rate_energy_partpeak
        (4) rate_energy_offpeak
        (5) rate_demand_peak
        (6) rate_demand_partpeak
        (7) rate_demand_overall
    """

    county = models.ForeignKey(County, on_delete=models.CASCADE)
    rate_energy_peak = models.FloatField(validators=[validate_positive])
    rate_energy_partpeak = models.FloatField(validators=[validate_positive])
    rate_energy_offpeak = models.FloatField(validators=[validate_positive])
    rate_demand_peak = models.FloatField(validators=[validate_positive])
    rate_demand_partpeak = models.FloatField(validators=[validate_positive])
    rate_demand_overall = models.FloatField(validators=[validate_positive])

    class Meta:
        db_table = 'script_config_load_controller'
        unique_together = (('county',
                            'rate_energy_peak',
                            'rate_energy_partpeak',
                            'rate_energy_offpeak',
                            'rate_demand_peak',
                            'rate_demand_partpeak',
                            'rate_demand_overall'),)


class LoadForecastConfig(models.Model):
    """Algorithm: EV Load Forecast inputs:
        (0) config_name
        (1) aggregation_level
        (2) num_evs
        (3) choice, which should base on which kind of aggregation level selected
        (4) fast_percent
        (5) work_percent
        (6) res_percent
        (7) l1_percent
        (8) public_l2_percent
    """

    config_name = models.CharField(max_length=100, blank=False, primary_key=True)
    aggregation_level = models.CharField(max_length=10, choices=AggregationLevel.choices(), default=AggregationLevel.COUNTY)
    num_evs = models.IntegerField(validators=[validate_positive])
    # TODO: how validate choice and aggregation together at model level rather than serializer level?
    choice = models.CharField(max_length=30)
    fast_percent = models.FloatField()
    work_percent = models.FloatField()
    res_percent = models.FloatField()
    l1_percent = models.FloatField()
    public_l2_percent = models.FloatField()

    class Meta:
        db_table = 'script_config_ev_load_forecast'
        unique_together = (('aggregation_level',
                            'num_evs',
                            'choice',
                            'fast_percent',
                            'work_percent',
                            'res_percent',
                            'l1_percent',
                            'public_l2_percent'),)


class LoadProfileConfig(models.Model):
    """Algorithm: Load Profile inputs:
        (1) lf_config of LoadForecastConfig
        (2) poi
        (3) year
        (4) day_type
    """

    lf_config = models.ForeignKey(LoadForecastConfig, on_delete=models.CASCADE)
    poi = models.CharField(max_length=20, choices=POI.choices(), default=POI.UNKNOWN)
    year = models.IntegerField()
    day_type = models.CharField(max_length=20, choices=DayType.choices(), default=DayType.WEEKDAY)

    class Meta:
        db_table = 'script_config_cba_load_profile'
        unique_together = (('lf_config',
                            'poi',
                            'year',
                            'day_type'),)


class GasConsumptionConfig(models.Model):
    """Algorithm: Gas Consumption inputs:
        (1) lf_config of LoadForecastConfig
        (2) year
    """

    lf_config = models.ForeignKey(LoadForecastConfig, on_delete=models.CASCADE)
    year = models.IntegerField()

    class Meta:
        db_table = 'script_config_cba_gas_consumption'
        unique_together = (('lf_config',
                            'year'),)


class CostBenefitConfig(models.Model):
    """Algorithm: Cost Benefit inputs:
        (1) lf_config of LoadForecastConfig
        (2) year
    """

    lf_config = models.ForeignKey(LoadForecastConfig, on_delete=models.CASCADE)
    year = models.IntegerField()

    class Meta:
        db_table = 'script_config_cba_cost_benefit'
        unique_together = (('lf_config',
                            'year'),)


class NetPresentValueConfig(models.Model):
    """Algorithm: Net Present Value inputs:
        (1) lf_config of LoadForecastConfig
        (2) year
    """

    lf_config = models.ForeignKey(LoadForecastConfig, on_delete=models.CASCADE)
    year = models.IntegerField()

    class Meta:
        db_table = 'script_config_cba_net_present_value'
        unique_together = (('lf_config',
                            'year'),)


class EmissionConfig(models.Model):
    """Algorithm: Emission inputs:
        (1) lf_config of LoadForecastConfig
        (2) year
    """

    lf_config = models.ForeignKey(LoadForecastConfig, on_delete=models.CASCADE)
    year = models.IntegerField()

    class Meta:
        db_table = 'script_config_cba_emission'
        unique_together = (('lf_config',
                            'year'),)
