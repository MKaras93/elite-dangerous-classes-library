from decimal import Decimal


class System:
    def __init__(self, name: str):
        self.name = name


class Faction:
    def __init__(self, name: str):
        self.name = name


class FactionBranch:
    def __init__(self, faction: Faction, system: System, is_main: bool = False, influence: Decimal = 0):
        self.faction = faction
        self.system = system
        self.is_main = is_main
        self.influence = influence


class OrbitalStation:
    def __init__(self, name, station_type, system, distance_to_arrival, services, controlling_faction):
        self.name = name
        self.station_type = station_type
        self.system = system
        self.distance_to_arrival = distance_to_arrival
        self.services = services
        self.controlling_faction = controlling_faction
