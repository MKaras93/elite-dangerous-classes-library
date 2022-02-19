import edclasses


def get_orbital_station(
    name,
    station_type,
    system,
    distance_to_arrival=None,
    services=None,
    controlling_faction=None,
):
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
    return edclasses.FactionBranch.create(faction=faction, system=system)


def get_system(name):
    return edclasses.System.create(name=name)
