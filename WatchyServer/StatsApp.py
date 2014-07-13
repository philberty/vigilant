import os

from flask import Flask
from flask import jsonify
from flask import render_template

StatSession_Logs = { }
StatSession_Hosts = { }
StatSession_Process = { }
StatSession_Metrics = { }

tfolder = os.path.join (os.path.dirname (os.path.abspath (__file__)), 'templates')
sfolder = os.path.join (os.path.dirname (os.path.abspath (__file__)), 'static')
app = Flask ('WatchyServer', template_folder=tfolder, static_folder=sfolder)

@app.route ("/")
def index ():
    return render_template ('index.html')

@app.route ("/process/<path:key>")
def processGraph (key):
    return render_template ('graph.html', node=key, prefix='/api/process/')

@app.route ("/hosts/<path:key>")
def hostsGraph (key):
    return render_template ('graph.html', node=key, prefix='/api/hosts/')

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
