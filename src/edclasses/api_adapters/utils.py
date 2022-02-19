from decimal import Decimal

import edclasses


def get_orbital_station(
    name,
    station_type,
    system,
    distance_to_arrival=None,
    services=None,
    controlling_faction=None,
):

    if isinstance(system, str):
        system = edclasses.System.create(name=system)

    if distance_to_arrival and not isinstance(distance_to_arrival, Decimal):
        distance_to_arrival = Decimal(distance_to_arrival)

    return edclasses.OrbitalStation.create(
        name=name,
        station_type=station_type,
        system=system,
        distance_to_arrival=distance_to_arrival,
        services=services,
        controlling_faction=controlling_faction,
    )


def get_faction(name):
    return edclasses.Faction.create(name=name)


def get_faction_branch(faction, system):
    if isinstance(system, str):
        system = edclasses.System.create(name=system)

    if isinstance(faction, str):
        faction = edclasses.Faction.create(name=faction)

    return edclasses.FactionBranch.create(faction=faction, system=system)


def get_system(name):
    return edclasses.System.create(name=name)
