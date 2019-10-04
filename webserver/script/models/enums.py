from enum import Enum

class EnumWithChoices(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class POI(EnumWithChoices):
    """Place of interest"""
    WP = 'Workplace'
    UK = 'Unknown'
    # [TODO] add more POIs


class POISub(EnumWithChoices):
    """Place of interest sub-category"""
    HT = 'High-Tech'
    UK = 'Unknown'
    # [TODO] add more POI sub-categories


class ChargingConnector(EnumWithChoices):
    """Charging connector type"""
    CHAdeMO = 'CHAdeMO'
    Combo = 'Combo'
    J1772 = 'J1772'
    UK = 'Unknown'
    # [TODO] add more connector types


class VehicleMake(EnumWithChoices):
    """Vehicle make"""
    Nissan = 'Nissan'
    Chevrolet = 'Chevrolet'
    Audi = 'Audi'
    BMW = 'BMW'
    Honda = 'Honda'
    UK = 'Unknown'
    # [TODO] add more vehicle makes


class EVType(EnumWithChoices):
    """EV type"""
    PLUGIN = 'PLUGIN'
    HYBRID = 'HYBRID'
    UK = 'UNKNOWN'
    # [TODO] add more EV types
