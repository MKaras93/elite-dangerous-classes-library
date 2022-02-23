from urllib import parse


import requests
from functools import lru_cache

from ratelimit import limits


class EliteBgsClient:
    API_URL = "https://elitebgs.app/api/ebgs/v5/"

    def __init__(self):
        self.session = requests.Session()

    @limits(calls=20, period=60)
    def _get_request(self, path="", **kwargs):
        url = parse.urljoin(self.API_URL, path)
        print(f"Shooting at {url} with params {kwargs}")
        response = self.session.get(url, params=kwargs)
        return response.json()

    @lru_cache  # TODO: replace this with a proper cache:
    # we should have a time expiring cache, would be best if we would save single objects from API response
    # (e.g. object representing faction presence) and then reuse that.
    def get_request(self, path="", **kwargs):
        return self._get_request(path, **kwargs)

    def factions(self, **kwargs):
        return self.get_request("factions", **kwargs)

    def stations(self, **kwargs):
        return self.get_request("stations", **kwargs)

    def systems(self, **kwargs):
        return self.get_request("systems", **kwargs)

    def ticks(self, **kwargs):
        return self.get_request("ticks", **kwargs)
