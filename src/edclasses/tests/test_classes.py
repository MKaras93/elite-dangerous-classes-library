from .factories.classes_factories import (
    SystemFactory,
    FactionFactory,
    FactionBranchFactory,
    OrbitalStationFactory,
)
from .. import System, Faction, enums


def test_system_factory():
    # TODO: remove, it's an exmaple test to check pytest and factory setup
    system = SystemFactory()
    assert system.name == "System"


def test_classes():
    # TODO: remove, it's an example test to check pytest and factory setup
    system = SystemFactory()
    faction = FactionFactory()
    faction_branch = FactionBranchFactory()
    station = OrbitalStationFactory()


class TestSystem:
    class TestCreateMethods:
        def test_create_branch_updates_related_objects(self):
            system: System = SystemFactory()
            faction: Faction = FactionFactory()

            faction_branch_1 = system.create_faction_branch(faction)
            faction_branch_2 = system.create_faction_branch(faction)

            assert faction_branch_1.system == system
            assert faction_branch_1.faction == faction
            assert system.faction_branches == {faction_branch_1, faction_branch_2}
            assert faction.faction_branches == {faction_branch_1, faction_branch_2}

        def test_create_station_updates_related_objects(self):
            system: System = SystemFactory()
            faction_branch = FactionBranchFactory(system=system)

            station = system.create_station(name="station", station_type=enums.StationType.STATION, controlling_faction=faction_branch)

            assert station.station_type == enums.StationType.STATION
            assert station.system == system
            assert station.controlling_faction == faction_branch
            assert faction_branch.stations == {station}
            assert system.stations == {station}
    class StationControllingFactionSetter:
