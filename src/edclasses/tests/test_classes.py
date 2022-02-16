from .factories.classes_factories import *


def test_system_factory():
    system = SystemFactory()
    assert system.name == "System 0"
