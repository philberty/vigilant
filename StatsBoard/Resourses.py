import sys
import requests


def get_host_stat_from_store(store, key):
    try:
        response = requests.get(store + '/api/host/liveness/' + key).json()
        resp = requests.get(store + '/api/host/rest/' + key)
        response['payload'] = resp.json()
    except:
        response = {'alive': False, 'error': 'Invalid data-store and or key'}
    finally:
        return response


def get_host_keys_from_store(store):
    try:
        resp = requests.get(store + '/api/host/keys')
        response = {'store': store, 'keys': resp.json()}
    except:
        response = {'store': store, 'error': str(sys.exc_info()[1])}
    finally:
        return response


def get_host_proc_state_from_store(store, host):
    try:
        resp = requests.get(store + '/api/host/procs/' + host)
        payload = []
        for i in resp.json():
            resp = requests.post(store + '/api/proc/rest/' + i)
            alive = requests.get(store + '/api/proc/liveness/' + i)
            payload.append({
                'alive': alive.json()['alive'],
                'payload': resp.json()
            })
        response = {'store': store, 'payload': payload}
    except:
        response = {'store': store, 'error': str(sys.exc_info()[1])}
    finally:
        return response


class DataStoreResources:
    def __init__(self, datastores):
        self._datastores = datastores

    def get_cluster_state(self):
        response = {}
        for i in self._datastores:
            state = i + '/api/state'
            resp = requests.get(state)
            if resp.ok:
                response[str(i)] = resp.json()
        return response
