from decimal import Decimal
from typing import Optional, List, Set

import edclasses.api_adapters.elite_bgs_adapter as bgs_adapter
from . import enums
from .utils import UniqueInstanceMixin, OneToOneRelation


class System(UniqueInstanceMixin):
    keys = ("name",)
    registry = {}
    _station_relation = OneToOneRelation.create(parent_class_name="System", child_class_name="OrbitalStation")

    def __init__(self, name: str, station=None):
        self.name = name
        self.station = station
        super().__init__()

    def __repr__(self):
        return f"System '{self.name}'"

    def _station_setter(self, value):
        self._station_relation.set_for_parent(self, value)

    def _station_getter(self):
        return self._station_relation.get_for_parent(self)

    station = property(fget=_station_getter, fset=_station_setter)

class Faction(UniqueInstanceMixin):
    keys = ("name",)
    registry = {}

    def __init__(self, name: str):
        self.name = name
        self._faction_branches = set()
        super().__init__()

    def __repr__(self):
        return f"Faction '{self.name}'"

    @property
    def faction_branches(self) -> Set["FactionBranch"]:
        return self._faction_branches


class FactionBranch(UniqueInstanceMixin):
    keys = (
        "faction",
        "system",
    )
    registry = {}
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

    def delete(self):
        try:
            self._faction._faction_branches.remove(self)
            self._system._faction_branches.remove(self)
            del self
        except KeyError:
            super().delete()

    @property
    def faction(self) -> Faction:
        return self._faction

    @property
    def system(self) -> System:
        return self._system

    @property
    def stations(self) -> Set["OrbitalStation"]:
        return self._stations


class OrbitalStation(UniqueInstanceMixin):
    keys = (
        "name",
        "system",
    )
    registry = {}
    _system_relation = OneToOneRelation.create(parent_class_name="System", child_class_name="OrbitalStation")

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

    @property
    def controlling_faction(self) -> FactionBranch:
        return self._controlling_faction

    @controlling_faction.setter
    def controlling_faction(self, faction_branch: FactionBranch):
        if faction_branch is self._controlling_faction:
            return

        if self._controlling_faction and self._controlling_faction is not faction_branch:
            self._controlling_faction._stations.remove(self)
            if faction_branch is not None:
                faction_branch._stations.add(self)
        self._controlling_faction = faction_branch

    def _system_setter(self, value):
        self._system_relation.set_for_child(self, value)

    def _system_getter(self):
        return self._system_relation.get_for_child(self)

    system = property(fget=_system_getter, fset=_system_setter)
