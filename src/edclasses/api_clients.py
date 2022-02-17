from urllib import parse


import requests
from functools import lru_cache


class EliteBgsClient:
    API_URL = "https://elitebgs.app/api/ebgs/v5/"

    @lru_cache  # TODO: replace this with a proper cache:
    # we should have a time expiring cache, would be best if we would save single objects from API response
    # (e.g. object representing faction presence) and then reuse that.
    def get_request(self, path="", **kwargs):
        url = parse.urljoin(self.API_URL, path)
        response = requests.get(url, params=kwargs)
        return response.json()

    def factions(self, **kwargs):
        return self.get_request("factions", **kwargs)

    def stations(self, **kwargs):
        return self.get_request("stations", **kwargs)

    def systems(self, **kwargs):
        return self.get_request("systems", **kwargs)

    def ticks(self, **kwargs):
        return self.get_request("ticks", **kwargs)
