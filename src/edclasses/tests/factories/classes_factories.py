import factory

from ...models import SystemModel, FactionModel, FactionBranchModel, OrbitalStationModel
from ...enums import StationType


class SystemFactory(factory.Factory):
    class Meta:
        model = SystemModel

    name = factory.Sequence(lambda n: f"System {n}")


class FactionFactory(factory.Factory):
    class Meta:
        model = FactionModel

    name = factory.Sequence(lambda n: f"Faction {n}")


class FactionBranchFactory(factory.Factory):
    class Meta:
        model = FactionBranchModel

    faction = factory.SubFactory(FactionFactory)
    system = factory.SubFactory(SystemFactory)
    stations = list()
    is_main = False  # we don't need to know faction's main branch - usually we won't have this information
    influence = 50


class OrbitalStationFactory(factory.Factory):
    class Meta:
        model = OrbitalStationModel

    name = factory.Sequence(lambda n: f"Orbital Station {n}")
    station_type = StationType.STATION
    system = factory.SubFactory(SystemFactory)
    distance_to_arrival = 100
    services = list()
    controlling_faction = factory.SubFactory(FactionBranchFactory)
