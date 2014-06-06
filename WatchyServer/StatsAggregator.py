import sys
import json
import socket
import select
import threading
import traceback
import ServerUtil

from datetime import datetime

from BackendUtil import AsyncBackend
from BackendUtil import BackendDispatch
from StatsServer import StatSession_Logs
from StatsServer import StatSession_Hosts
from StatsServer import StatSession_Process
from StatsServer import StatSession_Metrics

def consumer (func):
    def decorated (*args, **kwargs):
        key = kwargs ['key']
        data = kwargs ['data']
        dtype = data ['type']
        rdata = json.dumps (data, sort_keys=True, indent=4, separators=(',', ': '))
        BackendDispatch.put ((key, dtype, rdata))
        func (*args, key=key, data=data)
    return decorated

class UDPStatsServer (threading.Thread):
    def __init__ (self, host='localhost', port=8080, climit=40, backends=[]):
        """
        Initilize Server keywords host default localhost and port 8080
        """
        threading.Thread.__init__ (self)
        self.host = host
        self.port = port
        self.running = False
        self.daemon = True
        self.climit = climit
        self.backend = AsyncBackend (backends)
        self.serverSocket = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.setblocking (0)

    @consumer
    def consumeProcess (self, key, data):
        if key not in StatSession_Process:
            StatSession_Process [key] = []
        if len (StatSession_Process [key]) >= self.climit:
            StatSession_Process [key] = StatSession_Process [key][1:]
        StatSession_Process [key].append (data)
    
    @consumer
    def consumeHost (self, key, data):
        if key not in StatSession_Hosts:
            StatSession_Hosts [key] = []
        if len (StatSession_Hosts [key]) >= self.climit:
            StatSession_Hosts [key] = StatSession_Hosts [key][1:]
        StatSession_Hosts [key].append (data)

    @consumer
    def consumeLog (self, key, data):
        if key not in StatSession_Logs:
            StatSession_Logs [key] = []
        if len (StatSession_Logs [key]) >= self.climit:
            StatSession_Logs [key] = StatSession_Logs [key][1:]
        StatSession_Logs [key].append (data)

    def consume (self, data):
        key = data ['name']
        which = data ['type']
        data ['timeStamp'] = datetime.strptime (data ['timeStamp'],
                                                '%Y%m%d%H%M%S').isoformat ()
        if which == 'host':
            self.consumeHost (key=key, data=data)
        elif which == 'process':
            self.consumeProcess (key=key, data=data)
        elif which == 'log':
            self.consumeLog (key=key, data=data)
        else:
            ServerUtil.warning ('Invalid type [%s]' % which)

    def run (self):
        ServerUtil.info ("Starting StatsAggregator on %s:%s" % (self.host, self.port))
        self.backend.start ()
        self.serverSocket.bind ((self.host, self.port))
        self.running = True
        inputs = [self.serverSocket]
        try:
            while len (inputs) > 0 and self.running is True:
                (reads, writes, errors) = select.select (
                    inputs, [], inputs
                )
                for i in reads:
                    rdata = i.recvfrom (256)
                    stats = rdata [0].strip ().rstrip ('\0')
                    try:
                        sobject = json.loads (stats)
                        sobject ['host'] = { 'host': rdata [1][0],
                                             'port': rdata [1][1]
                                         }
                        ServerUtil.debug ('Recieved [%s] from [%s:%i] for [%s]' \
                                         % (sobject ['type'],
                                            sobject ['host']['host'],
                                            sobject ['host']['port'],
                                            sobject ['name']))
                        self.consume (sobject)
                    except:
                        ServerUtil.debug ("%s" % traceback.format_exc ())
                        ServerUtil.debug ("[%s]" % stats)
                        ServerUtil.error ("%s" % sys.exc_info ()[1])
        except KeyboardInterrupt:
            ServerUtil.info ("Caught Keyboard interupt closing")
        except:
            ServerUtil.error ("%s" % traceback.format_exc ())
            ServerUtil.error ("%s" % sys.exc_info ()[1])
        finally:
            self.serverSocket.close ()
            ServerUtil.info ("Shutting down Backend")
            self.backend.running = False
            ServerUtil.info ("Stats Aggregator exited gracefully")

