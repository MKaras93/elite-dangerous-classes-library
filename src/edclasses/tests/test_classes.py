from .factories.classes_factories import (
    SystemFactory,
    FactionFactory,
    FactionBranchFactory,
    OrbitalStationFactory,
)
from .. import System, Faction, enums, FactionBranch


def test_system_factory():
    # TODO: remove, it's an exmaple test to check pytest and factory setup
    system = SystemFactory()
    assert system.name == "System 0"


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
            faction2: Faction = FactionFactory()

            faction_branch_1 = FactionBranchFactory(faction=faction, system=system)
            faction_branch_2 = FactionBranchFactory(faction=faction2, system=system)

            assert faction_branch_1.system == system
            assert faction_branch_1.faction == faction
            assert faction_branch_2.system == system
            assert faction_branch_2.faction == faction2
            assert system.faction_branches == [faction_branch_1, faction_branch_2]
            assert faction.faction_branches == [faction_branch_1]
            assert faction2.faction_branches == [faction_branch_2]

        def test_create_station_updates_related_objects(self):
            system: System = SystemFactory()
            faction_branch = FactionBranchFactory(system=system)

            station1 = OrbitalStationFactory(station_type=enums.StationType.STATION, controlling_faction=faction_branch, system=system)
            station2 = OrbitalStationFactory(station_type=enums.StationType.STATION, controlling_faction=faction_branch, system=system)

            assert station1.station_type == enums.StationType.STATION.value
            assert station1.system == system
            assert station1.controlling_faction == faction_branch
            assert station2.system == system
            assert station2.controlling_faction == faction_branch
            assert system.stations == [station1, station2]
            assert faction_branch.stations == [station1, station2]


class TestLinks:
    def test_links(self):
        system = SystemFactory()
        faction = FactionFactory(name="faction1")
        faction2 = FactionFactory(name="faction2")
        faction_branch = FactionBranchFactory(faction=faction, system=system)
        faction_branch2 = FactionBranchFactory(faction=faction2, system=system)
        assert system.faction_branches == [faction_branch, faction_branch2]
        assert faction.faction_branches == [faction_branch]
        assert faction2.faction_branches == [faction_branch2]
