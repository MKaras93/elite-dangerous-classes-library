from decimal import Decimal
from src.edclasses.api_clients.elite_bgs_client import EliteBgsClient


class EliteBgsAdapter:
    def __init__(self):
        self.client = EliteBgsClient()

    def influence(self, faction_branch: "FactionBranch") -> Decimal:
        faction_name = faction_branch.faction.name
        data = self.client.factions(name=faction_name)
        doc = data.get("docs", {})[0]
        faction_presence = doc["faction_presence"]
        faction_branch_data = next(
            faction
            for faction in faction_presence
            if faction["system_name_lower"] == faction_branch.system.name.lower()
        )

        return Decimal(faction_branch_data["influence"])
