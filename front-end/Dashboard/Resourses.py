import json
import requests


def get_aliveness_for_host(store, key) -> bool:
    resp = requests.get(store + '/api/hosts/liveness/' + key)
    return resp.json()['alive']


def get_host_stat_from_store(store, key) -> dict:
    resp = requests.get(store + '/api/hosts/rest/' + key)
    response = resp.json()
    response['alive'] = get_aliveness_for_host(store, key)
    return response


def get_host_head_stat_from_store(store, key) -> dict:
    resp = requests.get(store + '/api/hosts/head/' + key)
    response = resp.json()
    response['alive'] = get_aliveness_for_host(store, key)
    return response


def get_host_keys_from_store(store) -> dict:
    response = requests.get(store + '/api/hosts/keys')
    return response.json()


def get_host_state_from_store(store, key) -> dict:
    resp = requests.get(store + '/api/hosts/state/' + key)
    return resp.json()


def get_host_triggers_from_store(store, key) -> dict:
    resp = requests.get(store + '/api/hosts/triggers/' + key)
    return resp.json()


def delete_host_trigger_from_store(store, key) -> dict:
    resp = requests.delete(store + '/api/hosts/triggers/' + key)
    return resp.json()


def add_host_usage_trigger(store, payload) -> dict:
    headers = {'Content-type': 'application/json'}
    resp = requests.post(store + '/api/hosts/usage_trigger',
                        data=json.dumps(payload),
                        headers=headers)
    return resp.json()


def get_cluster_state(store) -> dict:
    resp = requests.get(store + '/api/state')
    return resp.json()


def get_hosts_state(store) -> dict:
    resp = requests.get(store + '/api/hosts/state')
    return resp.json()
