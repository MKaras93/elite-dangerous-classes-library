import datetime
from decimal import Decimal
from functools import cached_property
from typing import Optional, List

from . import enums


class ExpiringCachedPropertyMixin:
    @staticmethod
    def _get_expiration_key(item):
        return f"{item}_expiration_time"

    def _get_new_expiration_time(self, lifetime_in_seconds):
        if lifetime_in_seconds:
            return datetime.datetime.utcnow() + datetime.timedelta(seconds=lifetime_in_seconds)
        else:
            return None

    @staticmethod
    def _is_expired(expiration_time):
        if expiration_time and datetime.datetime.utcnow() >= expiration_time:
            return True
        return False

    def __getattribute__(self, item):
        get_attr = super().__getattribute__
        registry = get_attr("expiring_properties_registry")
        try:
            item_lifetime = registry[item]
        except KeyError:
            return get_attr(item)

        print("running machinery")
        cache = get_attr("__dict__")
        expiration_key = get_attr("_get_expiration_key")(item)
        expiration_time = cache.get(expiration_key)
        time_expired = expiration_time and datetime.datetime.utcnow() >= expiration_time
        if time_expired:
            cache.pop(item, None)

        val = super().__getattribute__(item)
        if not expiration_time or time_expired:
            cache[expiration_key] = get_attr("_get_new_expiration_time")(lifetime_in_seconds=item_lifetime)
        return val


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
    ):
        self.faction = faction
        self.system = system
        self.is_main = is_main
        self.influence = influence
        self.stations = stations or []

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
