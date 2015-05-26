import os

from . import Resourses

from flask import Flask
from flask import jsonify
from flask import request


public = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'www')
app = Flask(__name__, static_folder=public)


@app.errorhandler(Exception)
def not_found(error=None):
    message = {'message': 'Not Found: ' + request.url,
               'error': str(error)}
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/<path:path>")
def public(path):
    return app.send_static_file(path)


@app.route("/api/state")
def state():
    store = request.args.get('store')
    return jsonify(Resourses.get_cluster_state(store))


@app.route("/api/hosts/state")
def hosts_state():
    store = request.args.get('store')
    return jsonify(Resourses.get_hosts_state(store))


@app.route("/api/hosts/state/<key>")
def hosts_process_state(key):
    store = request.args.get('store')
    return jsonify(Resourses.get_host_state_from_store(store, key))


@app.route("/api/hosts/triggers/<key>", methods=['GET', 'DELETE'])
def host_triggers(key):
    store = request.args.get('store')
    if request.method == 'GET':
        return jsonify(Resourses.get_host_triggers_from_store(store, key))
    else:
        return jsonify(Resourses.delete_host_trigger_from_store(store, key))


@app.route("/api/hosts/usage_trigger", methods=['POST'])
def add_host_usage_trigger():
    store = request.args.get('store')
    return jsonify(Resourses.add_host_usage_trigger(store, request.get_json()))


@app.route("/api/hosts/keys")
def host_keys():
    store = request.args.get('store')
    return jsonify(Resourses.get_host_keys_from_store(store))


@app.route("/api/hosts/head/<key>")
def host_head_stat(key):
    store = request.args.get('store')
    return jsonify(Resourses.get_host_head_stat_from_store(store, key))


@app.route("/api/hosts/rest/<key>")
def host_rest_stat(key):
    store = request.args.get('store')
    return jsonify(Resourses.get_host_stat_from_store(store, key))
