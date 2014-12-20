import os

from . import Resourses

from flask import Flask
from flask import jsonify
from flask import request

from flask.ext.cache import Cache

public = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'www')
app = Flask(__name__, static_folder=public)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
resources = None

@app.errorhandler(404)
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
    return jsonify(resources.get_cluster_state())

@app.route("/api/host/keys")
def hostKeys():
    store = request.args.get('store')
    return jsonify(Resourses.get_host_keys_from_store(store))

@app.route("/api/host/<key>")
def hostStat(key):
    store = request.args.get('store')
    return jsonify(Resourses.get_host_stat_from_store(store, key))