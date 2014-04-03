import os
import sys
import json
import traceback
import ServerUtil

from flask import Flask
from flask import jsonify
from flask import render_template

from datetime import datetime

StatSession = { }
tfolder = os.path.join (os.path.dirname (os.path.abspath (__file__)), 'templates')
sfolder = os.path.join (os.path.dirname (os.path.abspath (__file__)), 'static')
app = Flask ('WatchyServer', template_folder=tfolder, static_folder=sfolder)

from StatsAggregator import UDPStatsServer

@app.route ("/")
def index ():
    return render_template ('index.html')

@app.route ("/api/keys")
def getKeys ():
    return jsonify ({'keys':StatSession.keys ()})

@app.route ("/api/graph/<path:key>")
def getGraph (key):
    if key not in StatSession:
        return jsonify ({'ready':False})
    data = []
    for i in StatSession [key]:
        ts = str (i ['timeStamp'])
        jts = datetime.strptime (ts, '%Y%m%d%H%M%S')
        gpair = (jts.isoformat (), i ['memory'])
        data.append (gpair)
    return jsonify ({ 'ready':True, 'data': data, 'len' : len (data),
                      'label':'Memory Usage of %s' % key
                  })

@app.route ("/api/data/<path:key>")
def getData (key):
    if key not in StatSession:
        return jsonify ({'data':None, 'len':0})
    return jsonify ({'data':StatSession [key], 'len':len (StatSession [key])})

@app.route ("/deps/<path:path>")
def staticJavaScript (path):
    return app.send_static_file (path)

class WatchyDServer:
    def __init__ (self, wbind='localhost', wport=8080, ubind='localhost', uport=8081, debug=False):
        self.web_bind = wbind
        self.web_port = wport
        self.debug = debug
        self.udp_server = UDPStatsServer (host=ubind, port=uport)

    def listen (self):
        global app
        try:
            self.udp_server.daemon = True
            self.udp_server.start ()
            app.run (host=self.web_bind, port=self.web_port)
        except:
            ServerUtil.error ("%s" % traceback.format_exc ())
            ServerUtil.error ("%s" % sys.exc_info ()[1])
        finally:
            ServerUtil.info ("Shutting down Stats Aggregator")
            self.udp_server.running = False
