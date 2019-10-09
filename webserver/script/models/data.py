from django.db import models
from script.models.enums import POI, POISub, ChargingConnector, VehicleMake, EVType
from script.validators import validate_positive

class County(models.Model):
    """County Info"""
    name = models.CharField(max_length=50, primary_key=True)
    residents = models.IntegerField(validators=[validate_positive])

    # [TODO] add other overviews of the county

    class Meta:
        db_table = 'script_county'


class ZipCode(models.Model):
    """Zip Code"""
    code = models.CharField(max_length=5, primary_key=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    class Meta:
        db_table = 'script_zip_code'


class ChargingStation(models.Model):
    """Charging station"""
    id = models.CharField(max_length=6, primary_key=True)
    zipcode = models.ForeignKey(ZipCode, on_delete=models.CASCADE)

    class Meta:
        db_table = 'script_charging_station'


class ChargingPort(models.Model):
    """Charging port"""
    id = models.CharField(max_length=6, primary_key=True)
    station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
    connector = models.CharField(max_length=20, choices=ChargingConnector.choices(), default=ChargingConnector.UK)

    class Meta:
        db_table = 'script_charging_port'


class Driver(models.Model):
    """Driver"""
    id = models.CharField(max_length=7, primary_key=True)
    zipcode = models.ForeignKey(ZipCode, on_delete=models.CASCADE)

    class Meta:
        db_table = 'script_driver'


class Vehicle(models.Model):
    """Vehicle"""
    make = models.CharField(max_length=20, choices=VehicleMake.choices(), default=VehicleMake.UK)
    model = models.CharField(max_length=30)
    year = models.IntegerField()
    battery_capacity = models.FloatField()
    ev_type = models.CharField(max_length=10, choices=EVType.choices(), default=EVType.UK)
    max_power = models.FloatField()

    class Meta:
        db_table = 'script_vehicle'


class ChargingSession(models.Model):
    """Charging session"""
    id = models.CharField(max_length=9, primary_key=True)
    start_time = models.DateTimeField() # default timezone PT
    end_time = models.DateTimeField()
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    session_time = models.IntegerField() # sec
    charging_time = models.IntegerField() # sec

    class Meta:
        db_table = 'script_charging_session'


class ChargingInterval(models.Model):
    """Charging interval"""
    id = models.CharField(max_length=9, primary_key=True)
    session = models.ForeignKey(ChargingSession, on_delete=models.CASCADE)
    peak_power = models.FloatField()
    avg_power = models.FloatField()
    energy = models.FloatField()
    start_time = models.DateTimeField()
    duration = models.IntegerField() # sec

    class Meta:
        db_table = 'script_charging_interval'
