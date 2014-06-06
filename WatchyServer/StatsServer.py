import os
import sys
import json
import traceback
import ServerUtil

from flask import Flask
from flask import jsonify
from flask import render_template

from gevent.pywsgi import WSGIServer

StatSession_Logs = { }
StatSession_Hosts = { }
StatSession_Process = { }
StatSession_Metrics = { }

tfolder = os.path.join (os.path.dirname (os.path.abspath (__file__)), 'templates')
sfolder = os.path.join (os.path.dirname (os.path.abspath (__file__)), 'static')
app = Flask ('WatchyServer', template_folder=tfolder, static_folder=sfolder)

from StatsAggregator import UDPStatsServer

@app.route ("/")
def index ():
    return render_template ('index.html')

@app.route ("/process/<path:key>")
def processGraph (key):
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

@app.route ("/api/process/keys")
def getProcess ():
    nodes = StatSession_Process.keys ()
    return jsonify ({'keys':nodes, 'len':len (nodes)})

@app.route ("/api/logs/keys")
def getLogs ():
    nodes = StatSession_Logs.keys ()
    return jsonify ({'keys':nodes, 'len':len (nodes)})

@app.route ("/api/process/graph/<path:key>")
def getProcessGraph (key):
    if key not in StatSession_Process:
        return jsonify ({'ready':False})
    data = []
    for i in StatSession_Process [key]:
        data.append ((i ['timeStamp'], i ['memory']))
    return jsonify ({ 'ready':True, 'len' : len (StatSession_Process [key]),
                      'label':'Memory Usage of %s' % key, 'data': data})

@app.route ("/api/process/data/<path:key>")
def getProcessData (key):
    if key not in StatSession_Process:
        return jsonify ({'data':None, 'len':0})
    return jsonify ({'data':StatSession_Process [key], 'len':len (StatSession_Process [key])})

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
    def __init__ (self, cacheLimit, backends, wbind='localhost', wport=8080,
                  ubind='localhost', uport=8081, debug=False):
        self.web_bind = wbind
        self.web_port = wport
        self.debug = debug
        self.udp_server = UDPStatsServer (host=ubind, port=uport,
                                          climit=cacheLimit, backends=backends)

    def listen (self):
        try:
            self.udp_server.start ()
            ServerUtil.info ('WSGIServer:[gevent] starting http://%s:%i/' \
                             % (self.web_bind, self.web_port))
            http_server = WSGIServer ((self.web_bind, self.web_port), app)
            http_server.serve_forever()
        except KeyboardInterrupt:
            ServerUtil.warning ('Caught keyboard interupt stopping')
        except:
            ServerUtil.error ("%s" % traceback.format_exc ())
            ServerUtil.error ("%s" % sys.exc_info ()[1])
        finally:
            ServerUtil.info ("Shutting down Stats Aggregator")
            self.udp_server.running = False
