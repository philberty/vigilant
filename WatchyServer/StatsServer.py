import os
import sys
import json
import traceback
import ServerUtil

from datetime import datetime

from flask import Flask
from flask import jsonify
from flask import render_template
from flask_sockets import Sockets

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

StatSession_Logs = { }
StatSession_Hosts = { }
StatSession_Metrics = { }

tfolder = os.path.join (os.path.dirname (os.path.abspath (__file__)), 'templates')
sfolder = os.path.join (os.path.dirname (os.path.abspath (__file__)), 'static')
app = Flask ('WatchyServer', template_folder=tfolder, static_folder=sfolder)
sockets = Sockets (app) # TODO websocket api for realtime data per key

from StatsAggregator import UDPStatsServer

@app.route ("/")
def index ():
    return render_template ('index.html')

@app.route ("/metrics/<path:key>")
def metricsGraph (key):
    return render_template ('graph.html', node=key)

@app.route ("/hosts/<path:key>")
def hostsGraph (key):
    return render_template ('host.html', node=key)

@app.route ("/logs/<path:key>")
def logsView (key):
    return render_template ('logs.html', node=key)

@app.route ("/api/hosts/keys")
def getHosts ():
    nodes = StatSession_Hosts.keys ()
    return jsonify ({'keys':nodes, 'len':len (nodes)})

@app.route ("/api/metrics/keys")
def getMetrics ():
    nodes = StatSession_Metrics.keys ()
    return jsonify ({'keys':nodes, 'len':len (nodes)})

@app.route ("/api/logs/keys")
def getLogs ():
    nodes = StatSession_Logs.keys ()
    return jsonify ({'keys':nodes, 'len':len (nodes)})

@app.route ("/api/metrics/graph/<path:key>")
def getMetricGraph (key):
    if key not in StatSession_Metrics:
        return jsonify ({'ready':False})
    data = []
    for i in StatSession_Metrics [key]:
        ts = str (i ['timeStamp'])
        jts = datetime.strptime (ts, '%Y%m%d%H%M%S')
        data.append ((jts.isoformat (), i ['memory']))
    return jsonify ({ 'ready':True, 'len' : len (StatSession_Metrics [key]),
                      'label':'Memory Usage of %s' % key, 'data': data})

@app.route ("/api/hosts/graph/<path:key>")
def getHostGraph (key):
    if key not in StatSession_Hosts:
        return jsonify ({'ready':False})
    data = []
    for i in StatSession_Hosts [key]:
        ts = str (i ['timeStamp'])
        jts = datetime.strptime (ts, '%Y%m%d%H%M%S')
        data.append ((jts.isoformat (), i ['memory']))
    return jsonify ({ 'ready':True, 'len' : len (StatSession_Hosts [key]),
                      'label':'Memory Usage of %s' % key, 'data': data})

@app.route ("/api/metrics/data/<path:key>")
def getMetricData (key):
    if key not in StatSession_Metrics:
        return jsonify ({'data':None, 'len':0})
    return jsonify ({'data':StatSession_Metrics [key], 'len':len (StatSession_Metrics [key])})

@app.route ("/api/hosts/data/<path:key>")
def getHostData (key):
    if key not in StatSession_Hosts:
        return jsonify ({'data':None, 'len':0})
    return jsonify ({'data':StatSession_Hosts [key], 'len':len (StatSession_Hosts [key])})

@app.route ("/api/logs/data/<path:key>")
def getLogData (key):
    if key not in StatSession_Logs:
        return jsonify ({'data':None, 'len':0})
    return jsonify ({'data':StatSession_Logs [key], 'len':len (StatSession_Logs [key])})

@app.route ("/deps/<path:path>")
def statics (path):
    return app.send_static_file (path)

class WatchyDServer:
    def __init__ (self, wbind='localhost', wport=8080, ubind='localhost', uport=8081, debug=False):
        self.web_bind = wbind
        self.web_port = wport
        self.debug = debug
        self.udp_server = UDPStatsServer (host=ubind, port=uport)

    def listen (self):
        try:
            self.udp_server.daemon = True
            self.udp_server.start ()
            ServerUtil.info ('WSGIServer:[gevent] starting http://%s:%i/' \
                             % (self.web_bind, self.web_port))
            http_server = WSGIServer ((self.web_bind, self.web_port),
                                      app, handler_class = WebSocketHandler)
            http_server.serve_forever()
        except KeyboardInterrupt:
            ServerUtil.warning ('Caught keyboard interupt stopping')
        except:
            ServerUtil.error ("%s" % traceback.format_exc ())
            ServerUtil.error ("%s" % sys.exc_info ()[1])
        finally:
            ServerUtil.info ("Shutting down Stats Aggregator")
            self.udp_server.running = False
