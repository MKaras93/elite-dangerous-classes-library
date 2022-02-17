from decimal import Decimal
from typing import List

from .utils import get_orbital_station, get_faction_branch, get_faction, get_system
from .. import enums
from ..api_clients import EliteBgsClient
from ..utils import return_first_match

ELITE_BGS_CLIENT = EliteBgsClient()

class EliteBgsAdapterBase:
    def __init__(self):
        self.client = ELITE_BGS_CLIENT

    def _convert_station_dict_to_obj(self, station_dict: dict) -> "OrbitalStation":
        station_type = station_dict["type"]
        try:
            station_type_enum = enums.StationType(station_type)
        except ValueError:
            station_type_enum = enums.StationType.STATION

        return get_orbital_station(
            name=station_dict["name"],
            station_type=station_type_enum,
            system=station_dict["system"],
            distance_to_arrival=station_dict["distance_from_star"],
        )

    def _convert_faction_presence_dict_to_obj(
        self, faction_presence_dict: dict, faction_name: str
    ) -> "FactionBranch":
        faction = get_faction(name=faction_name)
        system = get_system(name=faction_presence_dict["system_name"])
        faction_branch = get_faction_branch(faction=faction, system=system)
        return faction_branch

    @staticmethod
    def _get_factions_from_response(response: dict) -> List:
        return response.get("docs", [])


class EliteBgsFactionBranchAdapter(EliteBgsAdapterBase):
    def influence(self, faction_branch: "FactionBranch") -> Decimal:
        faction_name = faction_branch.faction.name
        data = self.client.factions(name=faction_name)

        factions = data["docs"]
        faction = return_first_match(
            lambda fact: fact["name"].lower() == faction_name.lower(), factions
        )
        faction_presence_list = faction["faction_presence"]
        faction_presence = return_first_match(
            lambda fact: fact["system_name_lower"]
            == faction_branch.system.name.lower(),
            faction_presence_list,
        )

        return Decimal(faction_presence["influence"])

    def stations(self, faction_branch: "FactionBranch") -> List["OrbitalStation"]:
        faction_name = faction_branch.faction.name
        system_name = faction_branch.system.name
        data = self.client.stations(system=system_name)
        stations = data["docs"]

        faction_stations = filter(
            lambda station: station["controlling_minor_faction"].lower()
            == faction_name.lower(),
            stations,
        )

        station_objects = []
        for station in faction_stations:
            station_obj = self._convert_station_dict_to_obj(station)
            station_objects.append(station_obj)

        return station_objects


class EliteBgsSystemAdapter(EliteBgsAdapterBase):
    def faction_branches(self, system: "System"):
        system_name_lower = system.name.lower()
        data = self.client.factions(system=system.name)
        factions = data["docs"]

        faction_branches = []
        for faction in factions:
            faction_in_this_system = return_first_match(
                lambda fact: fact["system_name_lower"] == system_name_lower,
                faction["faction_presence"],
            )
            faction_branch_obj = self._convert_faction_presence_dict_to_obj(
                faction_presence_dict=faction_in_this_system,
                faction_name=faction["name"],
            )
            faction_branches.append(faction_branch_obj)

        return faction_branches

    def stations(self, system: "System") -> List["OrbitalStations"]:
        data = self.client.stations(system=system.name)
        stations = data["docs"]

        station_objects = []
        for station in stations:
            station_obj = self._convert_station_dict_to_obj(station)
            station_objects.append(station_obj)

        return station_objects


class EliteBgsFactionAdapter(EliteBgsAdapterBase):
    def faction_branches(self, faction_obj):
        data = self.client.factions(name=faction_obj.name)
        factions = data["docs"]

        faction_branches = []

        faction_data = return_first_match(
            lambda fact: fact["name"].lower() == faction_obj.name.lower(), factions
        )

        for faction_presence in faction_data["faction_presence"]:
            faction_branch_obj = self._convert_faction_presence_dict_to_obj(
                faction_presence_dict=faction_presence,
                faction_name=faction_obj.name,
            )
            faction_branches.append(faction_branch_obj)

        return faction_branches
