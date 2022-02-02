from decimal import Decimal
from typing import List

from .utils import get_orbital_station
from .. import enums
from ..api_clients import EliteBgsClient
from ..utils import return_first_match


class EliteBgsAdapterBase:
    def __init__(self):
        self.client = EliteBgsClient()


class EliteBgsFactionBranchAdapter(EliteBgsAdapterBase):
    # TODO: find a better way to map it.

    @staticmethod
    def _get_factions_from_response(response: dict) -> List:
        return response.get("docs", [])

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

    def _convert_station_dict_to_obj(self, station_dict: dict) -> "OrbitalStation":
        station_type = station_dict["system"]
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
