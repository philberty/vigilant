class DataStoreResources:
    def __init__(self, datastores, proxies={}):
        self._datastores = datastores

    def getHostsInfo(self):
        for i in self._datastores:
