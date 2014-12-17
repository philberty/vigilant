import requests


class DataStoreResources:
    def __init__(self, datastores):
        self._datastores = datastores

    def getHostsInfo(self):
        response = {}
        for i in self._datastores:
            state = i + '/api/state'
            resp = requests.get(state)
            if resp.ok:
                response[str(i)] = resp.json()
        return response

    def getHostKeysForStore(self, store):
        resp = requests.get(store + '/api/host/keys')
        return {'store': store, 'keys': resp.json()}
