from enum import Enum


class StationType(Enum):
    # these are types as found in Elite Bgs API.
    CRATER_OUTPOST = "crateroutpost"
    ORBIS = "orbis"
    CORIOLIS = "coriolis"
    BERNAL = "bernal"
    ASTEROID_BASE = "asteroidbase"
    OUTPOST = "outpost"
    CRATER_PORT = "craterport"
    OCELLUS = "ocellus"
    ON_FOOT_SETTLEMENT = "onfootsettlement"
    STATION = "station"  # fallback for unknown type
    # MEGASHIP = "mega ship" # TODO: handle megaships


class StationService(Enum):
    MISSIONS = "Missions"
