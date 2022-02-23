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
    PIONEERSUPPLIES = "pioneersupplies"
    SHOP = "shop"
    CONTACTS = "contacts"
    FLIGHTCONTROLLER = "flightcontroller"
    FACILITATOR = "facilitator"
    MATERIALTRADER = "materialtrader"
    APEXINTERSTELLAR = "apexinterstellar"
    CARRIERVENDOR = "carriervendor"
    AUTODOCK = "autodock"
    MISSIONSGENERATED = "missionsgenerated"
    STATIONOPERATIONS = "stationoperations"
    TUNING = "tuning"
    CREWLOUNGE = "crewlounge"
    POWERPLAY = "powerplay"
    ENGINEER = "engineer"
    SHIPYARD = "shipyard"
    SEARCHRESCUE = "searchrescue"
    REPAIR = "repair"
    COMMODITIES = "commodities"
    STATIONMENU = "stationmenu"
    MODULEPACKS = "modulepacks"
    TECHBROKER = "techbroker"
    SOCIALSPACE = "socialspace"
    DOCK = "dock"
    FRONTLINESOLUTIONS = "frontlinesolutions"
    LIVERY = "livery"
    OUTFITTING = "outfitting"
    REFUEL = "refuel"
    EXPLORATION = "exploration"
    BLACKMARKET = "blackmarket"
    MISSIONS = "missions"
    REARM = "rearm"
    BARTENDER = "bartender"
    VISTAGENOMICS = "vistagenomics"
