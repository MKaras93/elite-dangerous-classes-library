from urllib import parse

import requests


class EliteBgsClient:
    api_url = "https://elitebgs.app/api/ebgs/v5/"

    def get_request(self, path="", **kwargs):
        url = parse.urljoin(self.api_url, path)
        return requests.get(url, params=kwargs)

    def factions(self, **kwargs):
        return self.get_request("factions", **kwargs)
