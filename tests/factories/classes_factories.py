import factory
from edclasses import System


class SystemFactory(factory.Factory):
    class Meta:
        model = System

    name = "system_name"
