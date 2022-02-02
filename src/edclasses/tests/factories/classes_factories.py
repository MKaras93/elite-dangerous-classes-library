import factory

from ...classes import System, Faction, FactionBranch, OrbitalStation
from ...enums import StationType


class SystemFactory(factory.Factory):
    class Meta:
        model = System

    name = "System"


class FactionFactory(factory.Factory):
    class Meta:
        model = Faction

    name = "Faction"


class FactionBranchFactory(factory.Factory):
    class Meta:
        model = FactionBranch

    faction = factory.SubFactory(FactionFactory)
    system = factory.SubFactory(SystemFactory)
    is_main = False  # we don't need to know faction's main branch - usually we won't have this information
    influence = 50
    stations = list()


class OrbitalStationFactory(factory.Factory):
    class Meta:
        model = OrbitalStation

    name = "Orbital Station"
    station_type = StationType.CORIOLIS
    system = factory.SubFactory(SystemFactory)
    distance_to_arrival = 100
    services = list()
    controlling_faction = factory.SubFactory(FactionBranchFactory)
