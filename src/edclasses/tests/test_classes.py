from .factories.classes_factories import (
    SystemFactory,
    FactionFactory,
    FactionBranchFactory,
    OrbitalStationFactory,
)


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
