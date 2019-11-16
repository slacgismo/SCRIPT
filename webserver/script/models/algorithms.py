from django.db import models
from django.contrib.postgres.fields import JSONField
from script.models.data import County
from script.models.enums import DayType, POI, AggregationLevel
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


class LoadForecast(models.Model):
    """Algorithm: EV Load Forecast
        inputs:
            (1) aggregation_level
            (2) num_evs
            (3) choice, which should base on which kind of aggregation level selected
            (4) fast_percent
            (5) work_percent
            (6) res_percent
            (7) l1_percent
            (8) public_l2_percent
        outputs：
            (1) Residential L1 load
            (2) Residential L2 load
            (3) Residential MUD load
            (4) Work load
            (5) Fast load
            (6) Public L2 load
            (7) Total load
        visualizations:
            (1) Residential L1 (load - time)
            (2) Residential L2 (load - time)
            (3) Residential MUD (load - time)
            (4) Work (load - time)
            (5) Fast (load - time)
            (6) Public L2 (load - time)
            (7) Total (load - time)
    """

    aggregation_level = models.CharField(max_length=10, choices=AggregationLevel.choices(), default=AggregationLevel.COUNTY)
    num_evs = models.IntegerField(validators=[validate_positive])
    # TODO: how validate choice and aggregation together at model level rather than serializer level?
    choice = models.CharField(max_length=30)
    fast_percent = models.FloatField()
    work_percent = models.FloatField()
    res_percent = models.FloatField()
    l1_percent = models.FloatField()
    public_l2_percent = models.FloatField()
    residential_l1_load = JSONField()
    residential_l2_load = JSONField()
    residential_mud_load = JSONField()
    work_load = JSONField()
    fast_load = JSONField()
    public_l2_load = JSONField()
    total_load = JSONField()

    class Meta:
        db_table = 'script_algorithm_ev_load_forecast'
        unique_together = (('aggregation_level',
                            'num_evs',
                            'choice',
                            'fast_percent',
                            'work_percent',
                            'res_percent',
                            'l1_percent',
                            'public_l2_percent'),)


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
            (1) gasoline consumption/emissions as well as EV share of the given year
        visualizations:
            TODO @Yanqing @Xinyi
    """

    year = models.IntegerField()
    consumption = JSONField()

    class Meta:
        db_table = 'script_algorithm_cba_gas_consumption'
        unique_together = (('year',),)


class CostBenefit(models.Model):
    """Algorithm: Cost Benefit Analysis of Cost/Benefit including
            Utility Bills
            Utility Bills (res)
            Utility Bills (work)
            Utility Bills (pub L2)
            Utility Bills (DCFC)
            Incremental upfront vehicle cost
            Charging infrastructure cost
            Charging infrastructure cost (res)
            Charging infrastructure cost (work L2)
            Charging infrastructure cost (public L2)
            Charging infrastructure cost (DCFC)
            Avoided vehicle gasoline ($)
            Avoided vehicle gasoline (gallons)
            Vehicle O&M Savings
            Federal EV Tax Credit
            Vehicle sales
            Transmission and Distribution Cost
            Distribution Cost
            Transmission Cost
            Cumulative personal light-duty EV population
            Cumulative personal light-duty LDV population
            EV sales as % of total personal light-duty vehicles
            Peak Demand 5-9 PM
            Energy Supply Cost
            Energy Cost
            Capacity Cost
        inputs:
            TODO
        outputs:
            (1) cost/benefit of the given year
        visualizations:
            TODO @Yanqing @Xinyi
    """

    year = models.IntegerField()
    cost_benefit = JSONField()

    class Meta:
        db_table = 'script_algorithm_cba_cost_benefit'
        unique_together = (('year',),)


class NetPresentValue(models.Model):
    """Algorithm: Cost Benefit Analysis of Net Present Value including
            Utility Bills
            Utility Bills (volumetric)
            Utility Bills (demand)
            Utility Bills (res)
            Utility Bills (work)
            Utility Bills (pub L2)
            Utility Bills (DCFC)
            Incremental upfront vehicle cost
            Charging infrastructure cost
            Charging infrastructure cost (res)
            Charging infrastructure cost (work L2)
            Charging infrastructure cost (public L2)
            Charging infrastructure cost (DCFC)
            Avoided vehicle gasoline
            Vehicle O&M Savings
            Federal EV Tax Credit
            Energy Supply Cost
            Energy Cost
            Generation Capacity Cost
            Vehicle Sales (NPV)
            Transmission and Distribution Cost
            Distribution Cost
            Transmission Cost
        inputs:
            TODO
        outputs:
            (1) NPV of the given year
        visualizations:
            TODO @Yanqing @Xinyi
    """

    year = models.IntegerField()
    npv = JSONField()

    class Meta:
        db_table = 'script_algorithm_cba_net_present_value'
        unique_together = (('year',),)


class Emission(models.Model):
    """Algorithm: Cost Benefit Analysis of Emissions including
            CO2 emissions
            NOX emissions
            PM 10 emissions
            SO2 emissions
            VOC emissions
        inputs:
            TODO
        outputs:
            (1) Emissions of the given year
        visualizations:
            TODO @Yanqing @Xinyi
    """

    year = models.IntegerField()
    emissions = JSONField()

    class Meta:
        db_table = 'script_algorithm_cba_net_emission'
        unique_together = (('year',),)
