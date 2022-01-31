import random
from decimal import Decimal
from functools import cached_property
from typing import Optional, List

from . import enums
from .commons.caching_utils import ExpiringCachedPropertyMixin

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
    # TODO: this should be handled automatically by decorator and metaclass, but not today.
    expiring_properties_registry = {
        "faction": DEFAULT_LIFETIME,
        "system": DEFAULT_LIFETIME,
        "is_main": DEFAULT_LIFETIME,
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
    def faction(self) -> Faction:
        raise NotImplemented

    @cached_property
    def system(self) -> System:
        return System(
            name=f"Dummy System {random.randint(0,1000)}"
        )  # TODO: to be replaced

    @cached_property
    def is_main(self) -> bool:
        raise NotImplemented

    @cached_property
    def influence(self) -> Decimal:
        raise NotImplemented

    @cached_property
    def stations(self) -> List["OrbitalStation"]:
        raise NotImplemented


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
