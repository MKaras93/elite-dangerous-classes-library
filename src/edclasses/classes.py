import random
from decimal import Decimal
from functools import cached_property
from typing import Optional, List

from . import enums
from .commons.caching_utils import ExpiringCachedPropertyMixin
from .api_adapters.elite_bgs_adapter import EliteBgsAdapter

DEFAULT_LIFETIME = 5


class System:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"System '{self.name}'"


class Faction:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Faction '{self.name}'"


class FactionBranch(ExpiringCachedPropertyMixin):
    adapter = EliteBgsAdapter()
    # TODO: this should be handled automatically by decorator and metaclass, but not today.
    expiring_properties_registry = {
        "influence": DEFAULT_LIFETIME,
        "stations": DEFAULT_LIFETIME,
    }

    def __init__(
        self,
        faction: Faction,
        system: System,
        is_main: bool = False,
        influence: Decimal = 0,
        stations: List["OrbitalStation"] = None,
    ):
        self.faction = faction
        self.system = system
        self.is_main = is_main
        self.influence = influence
        self.stations = stations or []

    def __repr__(self):
        return f"{self.faction} in {self.system}"

    @cached_property
    def influence(self) -> Decimal:
        return self.adapter.influence(self)

    @cached_property
    def stations(self) -> List["OrbitalStation"]:
        return self.adapter.stations(self)


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

    def __repr__(self):
        return f"{self.station_type.title()} '{self.name}'"
