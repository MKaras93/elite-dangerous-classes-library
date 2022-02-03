from decimal import Decimal
from typing import Optional, List

import edclasses.api_adapters.elite_bgs_adapter as bgs_adapter
from . import enums
from .utils import UniqueInstanceMixin


class System(UniqueInstanceMixin):
    keys = ("name",)

    def __init__(self, name: str):
        self.name = name
        self._stations = set()
        self._faction_branches = set()
        super().__init__()

    def __repr__(self):
        return f"System '{self.name}'"


class Faction(UniqueInstanceMixin):
    keys = ("name",)

    def __init__(self, name: str):
        self.name = name
        self._faction_branches = set()
        super().__init__()

    def __repr__(self):
        return f"Faction '{self.name}'"


class FactionBranch(UniqueInstanceMixin):
    keys = (
        "faction",
        "system",
    )
    adapter = bgs_adapter.EliteBgsFactionBranchAdapter()

    def __init__(
        self,
        faction: Faction,
        system: System,
        is_main: bool = False,
        influence: Decimal = None,
    ):
        self._faction = faction
        self._system = system
        self.is_main = is_main
        self.influence = influence
        self._stations = set()
        super().__init__()

    def __repr__(self):
        return f"{self._faction} in {self._system}"


class OrbitalStation(UniqueInstanceMixin):
    keys = (
        "name",
        "system",
    )

    def __init__(
        self,
        name: str,
        station_type: enums.StationType,
        system: System,
        distance_to_arrival: int,
        services: Optional[List] = None,
    ):
        self.name = name
        self.station_type = station_type.value
        self.system = system
        self.distance_to_arrival = distance_to_arrival
        self.services = services or []
        self._controlling_faction = None
        super().__init__()

    def __repr__(self):
        return f"{self.station_type.title()} '{self.name}'"
