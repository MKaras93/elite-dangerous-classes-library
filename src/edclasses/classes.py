from decimal import Decimal
from typing import Optional, List, Set

import edclasses.api_adapters.elite_bgs_adapter as bgs_adapter
from . import enums
from .utils import UniqueInstanceMixin, OneToManyRelation


class System(UniqueInstanceMixin):
    keys = ("name",)
    registry = {}
    _stations_relation = OneToManyRelation.create(parent_class_name="System", child_class_name="OrbitalStation")
    _faction_branches_relation = OneToManyRelation.create(parent_class_name="System", child_class_name="FactionBranch")

    def __init__(self, name: str, stations=None, faction_branches=None):
        self.name = name
        self.stations = stations or []
        self.faction_branches = faction_branches or []
        super().__init__()

    def __repr__(self):
        return f"System '{self.name}'"

    def _stations_setter(self, value):
        self._stations_relation.set_for_parent(self, value)

    def _stations_getter(self):
        return self._stations_relation.get_for_parent(self)

    stations = property(fget=_stations_getter, fset=_stations_setter)

    def _faction_branches_setter(self, value):
        self._faction_branches_relation.set_for_parent(self, value)

    def _faction_branches_getter(self):
        return self._faction_branches_relation.get_for_parent(self)

    faction_branches = property(fget=_faction_branches_getter, fset=_faction_branches_setter)

class Faction(UniqueInstanceMixin):
    keys = ("name",)
    registry = {}
    _faction_branches_relation = OneToManyRelation.create(parent_class_name="Faction", child_class_name="FactionBranch")

    def __init__(self, name: str):
        self.name = name
        super().__init__()

    def __repr__(self):
        return f"Faction '{self.name}'"

    def _faction_branches_setter(self, value):
        self._faction_branches_relation.set_for_parent(self, value)

    def _faction_branches_getter(self):
        return self._faction_branches_relation.get_for_parent(self)

    faction_branches = property(fget=_faction_branches_getter, fset=_faction_branches_setter)

class FactionBranch(UniqueInstanceMixin):
    keys = (
        "faction",
        "system",
    )
    registry = {}
    adapter = bgs_adapter.EliteBgsFactionBranchAdapter()
    _system_relation = OneToManyRelation.create(parent_class_name="System", child_class_name="FactionBranch")
    _faction_relation = OneToManyRelation.create(parent_class_name="Faction", child_class_name="FactionBranch")

    def __init__(
        self,
        faction: Faction,
        system: System,
        is_main: bool = False,
        influence: Decimal = None,
    ):
        self.faction = faction
        self.system = system
        self.is_main = is_main
        self.influence = influence
        self._stations = set()
        super().__init__()

    def __repr__(self):
        return f"{self.faction} in {self.system}"

    @property
    def stations(self) -> Set["OrbitalStation"]:
        return self._stations

    def _system_setter(self, value):
        self._system_relation.set_for_child(self, value)

    def _system_getter(self):
        return self._system_relation.get_for_child(self)

    system = property(fget=_system_getter, fset=_system_setter)

    def _faction_setter(self, value):
        self._faction_relation.set_for_child(self, value)

    def _faction_getter(self):
        return self._faction_relation.get_for_child(self)

    faction = property(fget=_faction_getter, fset=_faction_setter)


class OrbitalStation(UniqueInstanceMixin):
    keys = (
        "name",
        "system",
    )
    registry = {}
    _system_relation = OneToManyRelation.create(parent_class_name="System", child_class_name="OrbitalStation")

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
