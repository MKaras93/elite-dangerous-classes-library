from decimal import Decimal
from typing import Optional, List

import edclasses.api_adapters.elite_bgs_adapter as bgs_adapter
from . import enums
from .utils import UniqueInstanceMixin, OneToManyRelation, AutoRefreshMixin


class System(UniqueInstanceMixin, AutoRefreshMixin):
    keys = ("name",)
    registry = {}
    adapter = bgs_adapter.EliteBgsSystemAdapter()
    refreshed_fields = ("faction_branches", "stations")
    EXPIRATION_TIME_MINUTES = 5

    _stations_relation = OneToManyRelation.create(
        parent_class_name="System", child_class_name="OrbitalStation"
    )
    _faction_branches_relation = OneToManyRelation.create(
        parent_class_name="System", child_class_name="FactionBranch"
    )

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

    faction_branches = property(
        fget=_faction_branches_getter, fset=_faction_branches_setter
    )


class Faction(UniqueInstanceMixin, AutoRefreshMixin):
    keys = ("name",)
    registry = {}
    adapter = bgs_adapter.EliteBgsFactionAdapter()
    refreshed_fields = ("faction_branches",)
    EXPIRATION_TIME_MINUTES = 5

    _faction_branches_relation = OneToManyRelation.create(
        parent_class_name="Faction", child_class_name="FactionBranch"
    )

    def __init__(self, name: str):
        self.name = name
        super().__init__()

    def __repr__(self):
        return f"Faction '{self.name}'"

    def _faction_branches_setter(self, value):
        self._faction_branches_relation.set_for_parent(self, value)

    def _faction_branches_getter(self):
        return self._faction_branches_relation.get_for_parent(self)

    faction_branches = property(
        fget=_faction_branches_getter, fset=_faction_branches_setter
    )


class FactionBranch(UniqueInstanceMixin, AutoRefreshMixin):
    keys = (
        "faction",
        "system",
    )
    registry = {}
    adapter = bgs_adapter.EliteBgsFactionBranchAdapter()
    refreshed_fields = ("influence", "stations")
    EXPIRATION_TIME_MINUTES = 5

    _system_relation = OneToManyRelation.create(
        parent_class_name="System", child_class_name="FactionBranch"
    )
    _faction_relation = OneToManyRelation.create(
        parent_class_name="Faction", child_class_name="FactionBranch"
    )
    _stations_relation = OneToManyRelation.create(
        parent_class_name="FactionBranch", child_class_name="OrbitalStation"
    )

    def __init__(
        self,
        faction: Faction,
        system: System,
        is_main: bool = False,
        influence: Decimal = None,
        stations: List = None,
    ):
        self.faction = faction
        self.system = system
        self.is_main = is_main
        self.influence = influence
        self.stations = stations or []
        super().__init__()

    def __repr__(self):
        return f"{self.faction} in {self.system}"

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

    def _stations_setter(self, value):
        self._stations_relation.set_for_parent(self, value)

    def _stations_getter(self):
        return self._stations_relation.get_for_parent(self)

    stations = property(fget=_stations_getter, fset=_stations_setter)


class OrbitalStation(UniqueInstanceMixin, AutoRefreshMixin):
    keys = (
        "name",
        "system",
    )
    registry = {}
    adapter = bgs_adapter.EliteBgsStationAdapter()
    refreshed_fields = ("controlling_faction", "distance_to_arrival")
    EXPIRATION_TIME_MINUTES = 5

    _system_relation = OneToManyRelation.create(
        parent_class_name="System", child_class_name="OrbitalStation"
    )
    _controlling_faction_relation = OneToManyRelation.create(
        parent_class_name="FactionBranch", child_class_name="OrbitalStation"
    )

    def __init__(
        self,
        name: str,
        station_type: enums.StationType,
        system: System,
        distance_to_arrival: Optional[Decimal] = None,
        services: Optional[List] = None,
        controlling_faction=None,
    ):
        self.name = name
        self.station_type = station_type.value
        self.system = system
        self.distance_to_arrival = distance_to_arrival
        self.services = services or []
        self.controlling_faction = None or controlling_faction
        super().__init__()

    def __repr__(self):
        return f"{self.station_type.title()} '{self.name}'"

    def _system_setter(self, value):
        self._system_relation.set_for_child(self, value)

    def _system_getter(self):
        return self._system_relation.get_for_child(self)

    system = property(fget=_system_getter, fset=_system_setter)

    def _controlling_faction_setter(self, value):
        self._controlling_faction_relation.set_for_child(self, value)

    def _controlling_faction_getter(self):
        return self._controlling_faction_relation.get_for_child(self)

    controlling_faction = property(
        fget=_controlling_faction_getter, fset=_controlling_faction_setter
    )
