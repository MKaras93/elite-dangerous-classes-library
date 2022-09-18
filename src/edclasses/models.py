from decimal import Decimal
from typing import List, Optional

from . import enums
from .utils import UniqueInstanceMixin, OneToManyRelation


class SystemModel(UniqueInstanceMixin):
    keys = ("name",)
    registry = {}
    _stations_relation = OneToManyRelation.create(
        parent_class_name="System",
        child_class_name="OrbitalStation",
    )
    _faction_branches_relation = OneToManyRelation.create(
        parent_class_name="System",
        child_class_name="FactionBranch",
    )

    def __init__(
        self,
        name: str,
        stations=None,
        faction_branches=None,
        eddb_id=None,
        **kwargs,
    ):
        self.eddb_id = eddb_id
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

    stations = property(
        fget=_stations_getter,
        fset=_stations_setter,
    )

    def _faction_branches_setter(self, value):
        self._faction_branches_relation.set_for_parent(self, value)

    def _faction_branches_getter(self):
        return self._faction_branches_relation.get_for_parent(self)

    faction_branches = property(
        fget=_faction_branches_getter, fset=_faction_branches_setter
    )


class FactionModel(UniqueInstanceMixin):
    keys = ("name",)
    registry = {}

    _faction_branches_relation = OneToManyRelation.create(
        parent_class_name="Faction",
        child_class_name="FactionBranch",
    )

    def __init__(
        self,
        name: str,
        **kwargs,
    ):
        self.name = name
        super().__init__()

    def __repr__(self):
        return f"Faction '{self.name}'"

    def _faction_branches_setter(self, value):
        self._faction_branches_relation.set_for_parent(self, value)

    def _faction_branches_getter(self):
        return self._faction_branches_relation.get_for_parent(self)

    faction_branches = property(
        fget=_faction_branches_getter,
        fset=_faction_branches_setter,
    )


class FactionBranchModel(UniqueInstanceMixin):
    keys = (
        "faction",
        "system",
    )
    registry = {}

    _system_relation = OneToManyRelation.create(
        parent_class_name="System",
        child_class_name="FactionBranch",
    )
    _faction_relation = OneToManyRelation.create(
        parent_class_name="Faction",
        child_class_name="FactionBranch",
    )
    _stations_relation = OneToManyRelation.create(
        parent_class_name="FactionBranch",
        child_class_name="OrbitalStation",
    )

    def __init__(
        self,
        faction: FactionModel,
        system: SystemModel,
        is_main: bool = False,
        influence: Decimal = None,
        stations: List = None,
        active_states: List = None,
        pending_states: List = None,
        recovering_states: List = None,
        **kwargs,
    ):
        self.faction = faction
        self.system = system
        self.is_main = is_main
        self.influence = influence
        self.stations = stations or []
        self.active_states = active_states or []
        self.pending_states = pending_states or []
        self.recovering_states = recovering_states or []
        super().__init__()

    def __repr__(self):
        return f"{self.faction} in {self.system}"

    def _system_setter(self, value):
        self._system_relation.set_for_child(self, value)

    def _system_getter(self):
        return self._system_relation.get_for_child(self)

    system = property(
        fget=_system_getter,
        fset=_system_setter,
    )

    def _faction_setter(self, value):
        self._faction_relation.set_for_child(self, value)

    def _faction_getter(self):
        return self._faction_relation.get_for_child(self)

    faction = property(
        fget=_faction_getter,
        fset=_faction_setter,
    )

    def _stations_setter(self, value):
        self._stations_relation.set_for_parent(self, value)

    def _stations_getter(self):
        return self._stations_relation.get_for_parent(self)

    stations = property(
        fget=_stations_getter,
        fset=_stations_setter,
    )


class OrbitalStationModel(UniqueInstanceMixin):
    keys = (
        "name",
        "system",
    )
    registry = {}
    _system_relation = OneToManyRelation.create(
        parent_class_name="System",
        child_class_name="OrbitalStation",
    )
    _controlling_faction_relation = OneToManyRelation.create(
        parent_class_name="FactionBranch",
        child_class_name="OrbitalStation",
    )
    landing_pads_map = {enums.StationType.OUTPOST: enums.LandingPadSizes.MEDIUM}

    def __init__(
        self,
        name: str,
        station_type: enums.StationType,
        system: SystemModel,
        distance_to_arrival: Optional[Decimal] = None,
        services: Optional[List] = None,
        controlling_faction=None,
        state=None,
        **kwargs,
    ):
        self.name = name
        self.station_type = station_type
        self.system = system
        self.distance_to_arrival = distance_to_arrival
        self.services = services or []
        self.controlling_faction = None or controlling_faction
        self.state = state
        super().__init__()

    def __repr__(self):
        return f"{self.station_type.value.title()} '{self.name}'"

    def _system_setter(self, value):
        self._system_relation.set_for_child(self, value)

    def _system_getter(self):
        return self._system_relation.get_for_child(self)

    system = property(
        fget=_system_getter,
        fset=_system_setter,
    )

    def _controlling_faction_setter(self, value):
        self._controlling_faction_relation.set_for_child(
            self,
            value,
        )

    def _controlling_faction_getter(self):
        return self._controlling_faction_relation.get_for_child(self)

    controlling_faction = property(
        fget=_controlling_faction_getter,
        fset=_controlling_faction_setter,
    )

    @property
    def distance_to_arrival_rounded(self):
        return (
            int(round(self.distance_to_arrival, -2))
            if self.distance_to_arrival is not None
            else None
        )

    @property
    def max_landing_pad(self):
        return self.landing_pads_map.get(self.station_type, enums.LandingPadSizes.LARGE)
