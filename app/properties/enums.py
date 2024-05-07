from enum import unique

from django.db import models


@unique
class Availability(models.IntegerChoices):
    READY = 1, "Ready"
    UNDER_CONSTRUCTION = 2, "Under Construction"
    OTHER = 3, "Other"


@unique
class PhaseStatus(models.IntegerChoices):
    COMPLETED = 1, "Completed"
    NOT_COMPLETED = 2, "Not Completed"


class PropertyType(models.IntegerChoices):
    DTCP_PLOTS = 1, 'DTCP PLOTS'
    FARMLANDS = 2, 'Farmlands'
    FLAT = 3, 'Flat'
    VILLA = 4, 'Villa'


@unique
class AreaOfPurpose(models.IntegerChoices):
    RESIDENTIAL = 1, "Residential"
    COMMERCIAL = 2, "Commercial"


@unique
class AreaSizeUnit(models.IntegerChoices):
    SQ_FT = 1, "Sq Ft"
    YARDS = 2, "Yards"
    ACRES = 3, "Acres"
    GUNTALU = 4, "Guntalu"
    CENTS = 5, "Cents"
    ANKANALU = 6, "Ankanalu"


class Facing(models.IntegerChoices):
    NORTH = 1, 'North'
    SOUTH = 2, 'South'
    EAST = 3, 'East'
    WEST = 4, 'West'
    NORTHEAST = 5, 'Northeast'
    NORTHWEST = 6, 'Northwest'
    SOUTHEAST = 7, 'Southeast'
    SOUTHWEST = 8, 'Southwest'


class SoilType(models.IntegerChoices):
    RED = 1, 'Red'
    LOAMY = 2, 'Loamy'
    CLAY = 3, 'Clay'
    SANDY = 4, 'Sandy'
    PEATY = 5, 'Peaty'
    SILTY = 6, 'Silty'
    CHALKY = 7, 'Chalky'
    GRAVELLY = 8, 'Gravelly'
