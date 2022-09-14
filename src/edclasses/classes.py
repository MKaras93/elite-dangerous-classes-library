from .api_adapters.elite_bgs_adapter import (
    EliteBgsSystemAdapter,
    EliteBgsFactionAdapter,
    EliteBgsFactionBranchAdapter,
    EliteBgsStationAdapter,
)
from .models import SystemModel, FactionModel, FactionBranchModel, OrbitalStationModel
from .utils import AutoRefreshMixin


class System(AutoRefreshMixin, SystemModel):
    adapter = EliteBgsSystemAdapter()
    refreshed_fields = (
        "faction_branches",
        "stations",
        "eddb_id",
    )


class Faction(AutoRefreshMixin, FactionModel):
    adapter = EliteBgsFactionAdapter()
    refreshed_fields = ("faction_branches",)


class FactionBranch(AutoRefreshMixin, FactionBranchModel):
    adapter = EliteBgsFactionBranchAdapter()
    refreshed_fields = (
        "influence",
        "stations",
    )


class OrbitalStation(AutoRefreshMixin, OrbitalStationModel):
    adapter = EliteBgsStationAdapter()
    refreshed_fields = (
        "controlling_faction",
        "distance_to_arrival",
        "services",
    )
