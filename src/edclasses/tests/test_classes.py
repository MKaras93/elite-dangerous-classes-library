from .factories.classes_factories import *


class TestClassesRelations:
    def test_system_factory(self):
        system = SystemFactory()
        assert system.name == "System 0"
        assert system.stations == []
        assert system.faction_branches == []

    def test_station_system_relation(self):
        station = OrbitalStationFactory()
        system = station.system
        assert station.system == system
        assert system.stations == [station]

    def test_station_system_relation_when_station_is_created_with_ready_system(self):
        system = SystemFactory()
        station = OrbitalStationFactory(system=system)
        station2 = OrbitalStationFactory(system=system)
        assert station.system == system
        assert station2.system == system
        assert system.stations == [station, station2]

    def test_create_assigns_station_to_system_correctly(self):
        system = System.create(name="Test System", adapter=MOCKED_ADAPTER)
        station = OrbitalStation.create(
            system=system,
            name="Super Station",
            station_type=StationType.STATION,
            adapter=MOCKED_ADAPTER,
        )

        assert station.system == system
        assert system.stations == [station]

    def test_faction_branch_system_station_relations_are_updated_correctly(self):
        faction_branch = FactionBranchFactory()
        system = faction_branch.system
        orbital_station = OrbitalStationFactory(
            system=system, controlling_faction=faction_branch
        )

        assert faction_branch.system is system
        assert orbital_station.system is system
        assert orbital_station.controlling_faction is faction_branch
        assert system.faction_branches == [faction_branch]
        assert faction_branch.stations == [orbital_station]

    def test_faction_branch_faction_relation_is_updated_correctly(self):
        faction = FactionFactory()
        faction_branch = FactionBranchFactory(faction=faction)
        faction_branch_2 = FactionBranchFactory(faction=faction)

        assert faction_branch.faction == faction
        assert faction_branch_2.faction == faction
        assert faction.faction_branches == [faction_branch, faction_branch_2]
