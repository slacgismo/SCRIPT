from django.db import models
from django.contrib.postgres.fields import JSONField
from script.models.config import LoadControllerConfig, LoadForecastConfig, LoadProfileConfig, GasConsumptionConfig, CostBenefitConfig, NetPresentValueConfig, EmissionConfig
from script.validators import validate_positive, validate_year

# Create your models of algorithm results here.

class LoadController(models.Model):
    """Algorithm: Load Controller
        inputs:
            (1) config of LoadControllerConfig
        outputs：
            (1) uncontrolled load
            (2) controlled load (cvx optimized)
        visualizations:
            (1) uncontrolled load (load - time)
            (2) controlled load (cvx optimized) (load - time)
    """

    config = models.ForeignKey(LoadControllerConfig, on_delete=models.CASCADE, db_column="config")
    uncontrolled_load = JSONField()
    controlled_load = JSONField()

    class Meta:
        db_table = 'script_algorithm_load_controller'
        unique_together = (('config',),)


class LoadForecast(models.Model):
    """Algorithm: EV Load Forecast
        inputs:
            (1) config of LoadForecastConfig
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

    config = models.ForeignKey(LoadForecastConfig, on_delete=models.CASCADE, db_column="config")
    controlled = models.BooleanField()
    residential_l1_load = JSONField()
    residential_l2_load = JSONField()
    residential_mud_load = JSONField()
    work_load = JSONField()
    fast_load = JSONField()
    public_l2_load = JSONField()
    total_load = JSONField()

    class Meta:
        db_table = 'script_algorithm_ev_load_forecast'
        unique_together = (('config', 'controlled',),)


class LoadProfile(models.Model):
    """Algorithm: Cost Benefit Analysis of Load Profile
        inputs:
            (1) config of LoadProfileConfig
        outputs:
            (1) Aggregate/DCFC/Residential/Public L2/Workplace load profile throughout 24 hours of a weekday/weekend/peak
        visualizations:
            (1) Aggregate&DCFC&Residential&Public L2&Workplace load profile throughout 24 hours of a weekday&weekend&peak
    """

    config = models.ForeignKey(LoadProfileConfig, on_delete=models.CASCADE, db_column="config")
    uncontrolled_values = JSONField()
    controlled_values = JSONField()

    class Meta:
        db_table = 'script_algorithm_cba_load_profile'
        unique_together = (('config',),)


class GasConsumption(models.Model):
    """Algorithm: Cost Benefit Analysis of Annual Gas Consumption
        inputs:
            (1) config of GasConsumptionConfig
        outputs:
            (1) Gasoline Consumption (gallons) of the certain year
            (2) Gasoline Consumption (MMBTU) of the certain year
            (3) Gasoline Emissions (metric tons CO2) of the certain year
            (4) PHEV 10 Gasoline Consumption (gallons) of the certain year
            (5) PHEV 10 Gasoline Consumption (MMBTU) of the certain year
            (6) PHEV 10 Gasoline Emissions (metric tons CO2) of the certain year
            (7) PHEV 20 Gasoline Consumption (gallons) of the certain year
            (8) PHEV 20 Gasoline Consumption (MMBTU) of the certain year
            (9) PHEV 20 Gasoline Emissions (metric tons CO2) of the certain year
            (10) PHEV 40 Gasoline Consumption (gallons) of the certain year
            (11) PHEV 40 Gasoline Consumption (MMBTU) of the certain year
            (12) PHEV 40 Gasoline Emissions (metric tons CO2) of the certain year
            (13) BEV 100 Gasoline Consumption (gallons) of the certain year
            (14) BEV 100 Gasoline Consumption (MMBTU) of the certain year
            (15) BEV 100 Gasoline Emissions (metric tons CO2) of the certain year
            (16) EEV Share (%) of the certain year
        visualizations:
            (1) Gasoline Consumption (gallons) in the next several decades
            (2) Gasoline Consumption (MMBTU) in the next several decades
            (3) Gasoline Emissions (metric tons CO2) in the next several decades
            (4) PHEV 10 Gasoline Consumption (gallons) in the next several decades
            (5) PHEV 10 Gasoline Consumption (MMBTU) in the next several decades
            (6) PHEV 10 Gasoline Emissions (metric tons CO2) in the next several decades
            (7) PHEV 20 Gasoline Consumption (gallons) in the next several decades
            (8) PHEV 20 Gasoline Consumption (MMBTU) in the next several decades
            (9) PHEV 20 Gasoline Emissions (metric tons CO2) in the next several decades
            (10) PHEV 40 Gasoline Consumption (gallons) in the next several decades
            (11) PHEV 40 Gasoline Consumption (MMBTU) in the next several decades
            (12) PHEV 40 Gasoline Emissions (metric tons CO2) in the next several decades
            (13) BEV 100 Gasoline Consumption (gallons) in the next several decades
            (14) BEV 100 Gasoline Consumption (MMBTU) in the next several decades
            (15) BEV 100 Gasoline Emissions (metric tons CO2) in the next several decades
            (16) EEV Share (%) in the next several decades
    """

    config = models.ForeignKey(GasConsumptionConfig, on_delete=models.CASCADE, db_column="config")
    uncontrolled_values = JSONField()
    controlled_values = JSONField()

    class Meta:
        db_table = 'script_algorithm_cba_gas_consumption'
        unique_together = (('config',),)


class CostBenefit(models.Model):
    """Algorithm: Cost Benefit Analysis of Cost/Benefit
        inputs:
            (1) config of CostBenefitConfig
        outputs:
            (1) Utility Bills of the certain year
            (2) Utility Bills (res) of the certain year
            (3) Utility Bills (work) of the certain year
            (4) Utility Bills (pub L2) of the certain year
            (5) Utility Bills (DCFC) of the certain year
            (6) Incremental upfront vehicle cost of the certain year
            (7) Charging infrastructure cost of the certain year
            (8) Charging infrastructure cost (res) of the certain year
            (9) Charging infrastructure cost (work L2) of the certain year
            (10) Charging infrastructure cost (public L2) of the certain year
            (11) Charging infrastructure cost (DCFC) of the certain year
            (12) Avoided vehicle gasoline ($) of the certain year
            (13) Avoided vehicle gasoline (gallons) of the certain year
            (14) Vehicle O&M Savings of the certain year
            (15) Federal EV Tax Credit of the certain year
            (16) Vehicle sales of the certain year
            (17) Transmission and Distribution Cost of the certain year
            (18) Distribution Cost of the certain year
            (19) Transmission Cost of the certain year
            (20) Cumulative personal light-duty EV population of the certain year
            (21) Cumulative personal light-duty LDV population of the certain year
            (22) EV sales as % of total personal light-duty vehicles of the certain year
            (23) Peak Demand 5-9 PM of the certain year
            (24) Energy Supply Cost of the certain year
            (25) Energy Cost of the certain year
            (26) Capacity Cost of the certain year
        visualizations:
            (1) Utility Bills in the next several decades
            (2) Utility Bills (res) in the next several decades
            (3) Utility Bills (work) in the next several decades
            (4) Utility Bills (pub L2) in the next several decades
            (5) Utility Bills (DCFC) in the next several decades
            (6) Incremental upfront vehicle cost in the next several decades
            (7) Charging infrastructure cost in the next several decades
            (8) Charging infrastructure cost (res) in the next several decades
            (9) Charging infrastructure cost (work L2) in the next several decades
            (10) Charging infrastructure cost (public L2) in the next several decades
            (11) Charging infrastructure cost (DCFC) in the next several decades
            (12) Avoided vehicle gasoline ($) in the next several decades
            (13) Avoided vehicle gasoline (gallons) in the next several decades
            (14) Vehicle O&M Savings in the next several decades
            (15) Federal EV Tax Credit in the next several decades
            (16) Vehicle sales in the next several decades
            (17) Transmission and Distribution Cost in the next several decades
            (18) Distribution Cost in the next several decades
            (19) Transmission Cost in the next several decades
            (20) Cumulative personal light-duty EV population in the next several decades
            (21) Cumulative personal light-duty LDV population in the next several decades
            (22) EV sales as % of total personal light-duty vehicles in the next several decades
            (23) Peak Demand 5-9 PM in the next several decades
            (24) Energy Supply Cost in the next several decades
            (25) Energy Cost in the next several decades
            (26) Capacity Cost in the next several decades
    """

    config = models.ForeignKey(CostBenefitConfig, on_delete=models.CASCADE, db_column="config")
    uncontrolled_values = JSONField()
    controlled_values = JSONField()

    class Meta:
        db_table = 'script_algorithm_cba_cost_benefit'
        unique_together = (('config',),)


class NetPresentValue(models.Model):
    """Algorithm: Cost Benefit Analysis of Net Present Value

        inputs:
            (1) config of NetPresentValueConfig
        outputs:
            (1) NPV of Utility Bills by the certain year
            (2) NPV of Utility Bills (volumetric) by the certain year
            (3) NPV of Utility Bills (demand) by the certain year
            (4) NPV of Utility Bills (res) by the certain year
            (5) NPV of Utility Bills (work) by the certain year
            (6) NPV of Utility Bills (pub L2) by the certain year
            (7) NPV of Utility Bills (DCFC) by the certain year
            (8) NPV of Incremental upfront vehicle cost by the certain year
            (9) NPV of Charging infrastructure cost by the certain year
            (10) NPV of Charging infrastructure cost (res) by the certain year
            (11) NPV of Charging infrastructure cost (work L2) by the certain year
            (12) NPV of Charging infrastructure cost (public L2) by the certain year
            (13) NPV of Charging infrastructure cost (DCFC) by the certain year
            (14) NPV of Avoided vehicle gasoline by the certain year
            (15) NPV of Vehicle O&M Savings by the certain year
            (16) NPV of Federal EV Tax Credit by the certain year
            (17) NPV of Energy Supply Cost by the certain year
            (18) NPV of Energy Cost by the certain year
            (19) NPV of Generation Capacity Cost by the certain year
            (20) NPV of Vehicle Sales (NPV) by the certain year
            (21) NPV of Transmission and Distribution Cost by the certain year
            (22) NPV of Distribution Cost by the certain year
            (23) NPV of Transmission by the certain year
        visualizations:
            (1) NPV of Utility Bills by the certain year
            (2) NPV of Utility Bills (volumetric) by the certain year
            (3) NPV of Utility Bills (demand) by the certain year
            (4) NPV of Utility Bills (res) by the certain year
            (5) NPV of Utility Bills (work) by the certain year
            (6) NPV of Utility Bills (pub L2) by the certain year
            (7) NPV of Utility Bills (DCFC) by the certain year
            (8) NPV of Incremental upfront vehicle cost by the certain year
            (9) NPV of Charging infrastructure cost by the certain year
            (10) NPV of Charging infrastructure cost (res) by the certain year
            (11) NPV of Charging infrastructure cost (work L2) by the certain year
            (12) NPV of Charging infrastructure cost (public L2) by the certain year
            (13) NPV of Charging infrastructure cost (DCFC) by the certain year
            (14) NPV of Avoided vehicle gasoline by the certain year
            (15) NPV of Vehicle O&M Savings by the certain year
            (16) NPV of Federal EV Tax Credit by the certain year
            (17) NPV of Energy Supply Cost by the certain year
            (18) NPV of Energy Cost by the certain year
            (19) NPV of Generation Capacity Cost by the certain year
            (20) NPV of Vehicle Sales (NPV) by the certain year
            (21) NPV of Transmission and Distribution Cost by the certain year
            (22) NPV of Distribution Cost by the certain year
            (23) NPV of Transmission Cost by the certain year
    """

    config = models.ForeignKey(NetPresentValueConfig, on_delete=models.CASCADE, db_column="config")
    uncontrolled_values = JSONField()
    controlled_values = JSONField()

    class Meta:
        db_table = 'script_algorithm_cba_net_present_value'
        unique_together = (('config',),)


class Emission(models.Model):
    """Algorithm: Cost Benefit Analysis of Emissions
        inputs:
            (1) config of EmissionConfig
        outputs:
            (1) CO2 emissions of the certain year
            (2) NOX emissions of the certain year
            (3) PM 10 emissions of the certain year
            (4) SO2 emissions of the certain year
            (5) VOC emissions of the certain year
        visualizations:
            (1) CO2 emissions in the next several decades
            (2) NOX emissions in the next several decades
            (3) PM 10 emissions in the next several decades
            (4) SO2 emissions in the next several decades
            (5) VOC emissions in the next several decades
    """

    config = models.ForeignKey(EmissionConfig, on_delete=models.CASCADE, db_column="config")
    uncontrolled_values = JSONField()
    controlled_values = JSONField()

    class Meta:
        db_table = 'script_algorithm_cba_emission'
        unique_together = (('config',),)
