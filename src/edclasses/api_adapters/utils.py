from decimal import Decimal

# TODO: Fix ugly imports


def get_orbital_station(
    name,
    station_type,
    system,
    distance_to_arrival=None,
    services=None,
    controlling_faction=None,
):
    from edclasses import System, OrbitalStation

    if isinstance(system, str):
        system = System.create(name=system)

    if distance_to_arrival and not isinstance(distance_to_arrival, Decimal):
        distance_to_arrival = Decimal(distance_to_arrival)

    return OrbitalStation.create(
        name=name,
        station_type=station_type,
        system=system,
        distance_to_arrival=distance_to_arrival,
        services=services,
        controlling_faction=controlling_faction,
    )


def get_faction(name):
    from edclasses import Faction

    return Faction.create(name=name)


def get_faction_branch(faction, system):
    from edclasses import System, Faction, FactionBranch

    if isinstance(system, str):
        system = System.create(name=system)

    if isinstance(faction, str):
        faction = Faction.create(name=faction)

    return FactionBranch.create(faction=faction, system=system)


def get_system(name):
    from edclasses import System

    return System.create(name=name)
