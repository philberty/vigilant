import requests

from urllib.parse import quote as urlencode


class DataStoreResources:
    def __init__(self, datastores, proxies={}):
        self._proxies = proxies
        self._datastores = datastores

    def getHostsInfo(self):
        response = {}
        for i in self._datastores:
            state = i + '/state'
            resp = requests.get(state)
            response[urlencode(str(i))] = resp.json()
        return response
