import factory

from ...classes import System, Faction, FactionBranch, OrbitalStation
from ...enums import StationType


class SystemFactory(factory.Factory):
    class Meta:
        model = System

    name = factory.Sequence(lambda n: f"System {n}")


class FactionFactory(factory.Factory):
    class Meta:
        model = Faction

    name = factory.Sequence(lambda n: f"Faction {n}")


class FactionBranchFactory(factory.Factory):
    class Meta:
        model = FactionBranch

    faction = factory.SubFactory(FactionFactory)
    system = factory.SubFactory(SystemFactory)
    stations = list()
    is_main = False  # we don't need to know faction's main branch - usually we won't have this information
    influence = 50


class OrbitalStationFactory(factory.Factory):
    class Meta:
        model = OrbitalStation

    name = factory.Sequence(lambda n: f"Orbital Station {n}")
    station_type = StationType.STATION
    system = factory.SubFactory(SystemFactory)
    distance_to_arrival = 100
    services = list()
    controlling_faction = factory.SubFactory(FactionBranchFactory)
