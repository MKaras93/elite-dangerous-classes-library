from .factories.classes_factories import *


def test_system_factory():
    system = SystemFactory()
    assert system.name == "System 0"


def test_station_system_factory():
    station = OrbitalStationFactory()
    system = station.system
    assert station.system == system
    assert system.stations == [station]


def test_station_system_factory_2():
    system = SystemFactory()
    station = OrbitalStationFactory(system=system)
    assert station.system == system
    assert system.stations == [station]


def test_classes():
    system = System.create(name="aaa", adapter=MOCKED_ADAPTER)
    station = OrbitalStation.create(system=system, name="Super Station", station_type=StationType.STATION,
                                    adapter=MOCKED_ADAPTER)

    assert station.system == system
    assert system.stations == [station]


def test_faction_branches_stations():
    faction_branch = FactionBranchFactory()
    system = faction_branch.system
    orbital_station = OrbitalStationFactory(system=system, controlling_faction=faction_branch)

    assert faction_branch.system is system
    assert orbital_station.system is system
    assert orbital_station.controlling_faction is faction_branch
    assert system.faction_branches == [faction_branch]
    assert faction_branch.stations == [orbital_station]
