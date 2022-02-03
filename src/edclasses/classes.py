from decimal import Decimal
from typing import Optional, List

import edclasses.api_adapters.elite_bgs_adapter as bgs_adapter
from . import enums


class UniqueInstanceMixin:
    registry = {}
    keys = tuple()

    @classmethod
    def create(cls, **kwargs):
        try:
            return cls(**kwargs)
        except ValueError:
            return cls.get_from_registry(**kwargs)

    @classmethod
    def _get_key(cls, *args, **kwargs):
        return tuple(kwargs[attr] for attr in cls.keys)

    @classmethod
    def get_from_registry(cls, **kwargs):
        obj_key = cls._get_key(**kwargs)
        return cls.registry.get(obj_key)

    def __init__(self, *args, **kwargs):
        obj_key = self._get_key(**self.__dict__)
        obj = self.__class__.registry.get(obj_key)
        if obj is not None:
            raise ValueError
        self.__class__.registry[obj_key] = self
        super().__init__()


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
    keys = ("faction", "system",)
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
    keys = ("name", "system",)

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
