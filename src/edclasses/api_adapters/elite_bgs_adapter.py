from decimal import Decimal
from typing import List, Optional

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
    @staticmethod
    def _get_faction_data_from_response(response: dict, faction_name: str):
        factions = response.get("docs", [])
        faction_data = return_first_match(
            lambda fact: fact["name"].lower() == faction_name.lower(), factions
        )
        return faction_data

    @staticmethod
    def _get_faction_presence_from_faction_data(faction_data: dict, system_name: str):
        faction_presence_list = faction_data["faction_presence"]
        faction_presence = return_first_match(
            lambda fact: fact["system_name_lower"] == system_name.lower(),
            faction_presence_list,
        )
        return faction_presence

    def influence(self, faction_branch: "FactionBranch") -> Decimal:
        faction_name = faction_branch.faction.name
        data = self.client.factions(system=faction_branch.system.name)

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

    def _get_states(self, faction_branch, states_key):
        faction_name = faction_branch.faction.name
        system_name = faction_branch.system.name
        response = self.client.factions(system=system_name)
        faction_data = self._get_faction_data_from_response(response, faction_name)
        faction_presence = self._get_faction_presence_from_faction_data(faction_data, system_name)
        active_states = faction_presence.get(states_key, [])
        return [
            enums.State(state["state"])
            for state in active_states
        ]

    def active_states(self, obj):
        return self._get_states(obj, "active_states")

    def pending_states(self, obj):
        return self._get_states(obj, "pending_states")

    def recovering_states(self, obj):
        return self._get_states(obj, "recovering_states")

class EliteBgsSystemAdapter(EliteBgsAdapterBase):
    def faction_branches(self, system: "System"):
        system_name_lower = system.name.lower()
        # TODO: to save requests, it would be better to use client.system with factionDetails=True instead of factions,
        # because it's also used in system.eddb_id
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

    def eddb_id(self, system: "System") -> Optional[int]:
        # TODO: this could be taken from self.client.factions or stations - this way we would get more data.
        data = self.client.systems(name=system.name)
        systems = data["docs"]
        system_data = return_first_match(
            lambda syst: syst["name_lower"] == system.name.lower(),
            systems,
        )
        if system_data:
            return system_data["eddb_id"]
        return None


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


class EliteBgsStationAdapter(EliteBgsAdapterBase):
    def distance_to_arrival(self, obj):
        distance_to_arrival = self._get_this_station_data(
            obj=obj, key="distance_from_star"
        )

        if distance_to_arrival is not None:
            return Decimal(distance_to_arrival)
        return None

    def services(self, obj):
        services_data = self._get_this_station_data(obj=obj, key="services")

        services = [
            enums.StationService(service_dict["name_lower"])
            for service_dict in services_data
        ]
        return services

    def controlling_faction(self, obj):
        controlling_faction_name = self._get_this_station_data(
            obj=obj, key="controlling_minor_faction_cased"
        )
        faction = get_faction(controlling_faction_name)
        faction_branch = get_faction_branch(faction, obj.system)

        return faction_branch

    def state(self, obj):
        state_data = self._get_this_station_data(obj=obj, key="state")
        state = enums.State(state_data) if state_data != "none" else None
        return state

    def _get_this_station_data(self, obj: "OrbitalStation", key: str):
        data = self.client.stations(system=obj.system.name)

        stations = data["docs"]
        this_station_data = return_first_match(
            lambda station: station["name"].lower() == obj.name.lower(), stations
        )
        return this_station_data[key]

