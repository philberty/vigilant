import requests

from urllib.parse import quote as urlencode


class DataStoreResources:
    def __init__(self, datastores):
        self._datastores = datastores

    def getHostsInfo(self):
        response = {}
        for i in self._datastores:
            state = i + '/api/state'
            resp = requests.get(state)
            if resp.ok:
                response[urlencode(str(i))] = resp.json()
        return response
