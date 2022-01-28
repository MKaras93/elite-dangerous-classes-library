from enum import Enum


class StationType(Enum):
    CORIOLIS_STARPORT = "coriolis starport"
    OUTPOST = "outpost"
    MEGASHIP = "mega ship"
    PLANETARY_OUTPOST = "planetary outpost"


class StationService(Enum):
    MISSIONS = "Missions"
