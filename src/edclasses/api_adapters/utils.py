import edclasses


def get_orbital_station(
    name,
    station_type,
    system,
    distance_to_arrival=None,
    services=None,
    controlling_faction=None,
):
    return edclasses.OrbitalStation(
        name=name,
        station_type=station_type,
        system=system,
        distance_to_arrival=distance_to_arrival,
        services=services,
        controlling_faction=controlling_faction,
    )
