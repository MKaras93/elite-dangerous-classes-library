import datetime
from decimal import Decimal
from functools import cached_property
from typing import Optional, List

from . import enums
from .commons.caching_utils import ExpiringCachedPropertyMixin


class System:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"System '{self.name}'"


class Faction:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"Faction '{self.name}'"


class FactionBranch(ExpiringCachedPropertyMixin):
    # TODO: this should be handled automatically by decorator and metaclass, but not today.
    expiring_properties_registry = {"color": 5}

    def __init__(
        self,
        faction: Faction,
        system: System,
        is_main: bool = False,
        influence: Decimal = 0,
        stations: List["OrbitalStation"] = None,
        color="blue",
    ):
        self.faction = faction
        self.system = system
        self.is_main = is_main
        self.influence = influence
        self.stations = stations or []
        self.color = "blue"

    def __str__(self):
        return f"{self.faction} in {self.system}"

    @cached_property
    def color(self):
        # TODO: wip property, delete it
        return str(datetime.datetime.now())


class OrbitalStation:
    def __init__(
        self,
        name: str,
        station_type: enums.StationType,
        system: System,
        distance_to_arrival: int,
        services: Optional[List] = None,
        controlling_faction: Optional[
            FactionBranch  # TODO: would it be better to use Faction instead of FactionBranch?
        ] = None,
    ):
        self.name = name
        self.station_type = station_type.value
        self.system = system
        self.distance_to_arrival = distance_to_arrival
        self.services = services or []
        self.controlling_faction = controlling_faction

    def __str__(self):
        return f"{self.station_type.title()} '{self.name}'"
