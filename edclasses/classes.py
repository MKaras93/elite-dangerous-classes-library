from decimal import Decimal
from typing import Optional, List

from edclasses import enums

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


class FactionBranch:
    def __init__(
        self,
        faction: Faction,
        system: System,
        is_main: bool = False,
        influence: Decimal = 0,
        stations: List["OrbitalStation"] = None
    ):
        self.faction = faction
        self.system = system
        self.is_main = is_main
        self.influence = influence
        self.stations = stations or []

    def __str__(self):
        return f"{self.faction} in {self.system}"


class OrbitalStation:
    def __init__(
        self,
        name: str,
        station_type: enums.StationType,
        system: System,
        distance_to_arrival: int,
        services: list,
        controlling_faction: Optional[
            FactionBranch  # TODO: would it be better to use Faction instead of FactionBranch?
        ] = None,
    ):
        self.name = name
        self.station_type = station_type.value
        self.system = system
        self.distance_to_arrival = distance_to_arrival
        self.services = services
        self.controlling_faction = controlling_faction

    def __str__(self):
        return f"{self.station_type.title()} '{self.name}'"