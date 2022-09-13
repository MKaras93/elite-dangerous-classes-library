import factory

from ..mocked_adapter import MockedAdapter
from ...classes import System, Faction, FactionBranch, OrbitalStation
from ...enums import StationType

MOCKED_ADAPTER = MockedAdapter()


class EDModelFactoryBase(factory.Factory):
    adapter = MOCKED_ADAPTER


class SystemFactory(EDModelFactoryBase):
    class Meta:
        model = System

    name = factory.Sequence(lambda n: f"System {n}")


class FactionFactory(EDModelFactoryBase):
    class Meta:
        model = Faction

    name = factory.Sequence(lambda n: f"Faction {n}")


class FactionBranchFactory(EDModelFactoryBase):
    class Meta:
        model = FactionBranch

    faction = factory.SubFactory(FactionFactory)
    system = factory.SubFactory(SystemFactory)
    stations = list()
    is_main = False  # we don't need to know faction's main branch - usually we won't have this information
    influence = 50


class OrbitalStationFactory(EDModelFactoryBase):
    class Meta:
        model = OrbitalStation

    name = factory.Sequence(lambda n: f"Orbital Station {n}")
    station_type = StationType.STATION
    system = factory.SubFactory(SystemFactory)
    distance_to_arrival = 100
    services = list()
    controlling_faction = factory.SubFactory(FactionBranchFactory)
