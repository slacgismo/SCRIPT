from enum import Enum

class POI(Enum):
    """Place of interest"""
    WP = 'Workplace'
    UK = 'Unknown'
    # [TODO] add more POIs


class POISub(Enum):
    """Place of interest sub-category"""
    HT = 'High-Tech'
    UK = 'Unknown'
    # [TODO] add more POI sub-categories


class ChargingConnector(Enum):
    """Charging connector type"""
    CHAdeMO = 'CHAdeMO'
    Combo = 'Combo'
    J1772 = 'J1772'
    UK = 'Unknown'
    # [TODO] add more connector types


class VehicleMake(Enum):
    """Vehicle make"""
    Nissan = 'Nissan'
    Chevrolet = 'Chevrolet'
    Audi = 'Audi'
    BMW = 'BMW'
    Honda = 'Honda'
    UK = 'Unknown'
    # [TODO] add more vehicle makes


class EVType(Enum):
    """EV type"""
    PLUGIN = 'PLUGIN'
    HYBRID = 'HYBRID'
    UK = 'UNKNOWN'
    # [TODO] add more EV types
