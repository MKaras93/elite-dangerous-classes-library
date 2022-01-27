from tests.factories.classes_factories import SystemFactory


def test_system_factory():
    # TODO: remove, it's an exmaple test to check pytest and factory setup
    system = SystemFactory()
    assert system.name == "system_name"
