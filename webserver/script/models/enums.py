from enum import Enum

class EnumWithChoices(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class POI(EnumWithChoices):
    """Place of interest"""
    WP = 'Workplace'
    UNKNOWN = 'Unknown'
    # [TODO] add more POIs


class POISub(EnumWithChoices):
    """Place of interest sub-category"""
    HT = 'High-Tech'
    UNKNOWN = 'Unknown'
    # [TODO] add more POI sub-categories


class ChargingConnector(EnumWithChoices):
    """Charging connector type"""
    CHAdeMO = 'CHAdeMO'
    Combo = 'Combo'
    J1772 = 'J1772'
    UNKNOWN = 'Unknown'
    # [TODO] add more connector types


class VehicleMake(EnumWithChoices):
    """Vehicle make"""
    Nissan = 'Nissan'
    Chevrolet = 'Chevrolet'
    Audi = 'Audi'
    BMW = 'BMW'
    Honda = 'Honda'
    UNKNOWN = 'Unknown'
    # [TODO] add more vehicle makes


class EVType(EnumWithChoices):
    """EV type"""
    PLUGIN = 'PLUGIN'
    HYBRID = 'HYBRID'
    UNKNOWN = 'UNKNOWN'
    # [TODO] add more EV types
