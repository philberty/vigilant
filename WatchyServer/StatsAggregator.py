import sys
import json
import socket
import select
import threading
import traceback
import ServerUtil

from StatsServer import StatSession_Logs
from StatsServer import StatSession_Hosts
from StatsServer import StatSession_Metrics

def consumer (func):
    def decorated (*args, **kwargs):
        if hasattr (args [0], 'backend'):
            if args [0].backend is not None:
                args [0].backend.consume (*args, **kwargs)
        return func (*args, **kwargs)
    return decorated

class UDPStatsServer (threading.Thread):
    def __init__ (self, host='localhost', port=8080, climit=20, backend=None):
        """
        Initilize Server keywords host default localhost and port 8080
        """
        self.host = host
        self.port = port
        self.running = False
        self.climit = climit
        self.backend = backend
        self.serverSocket = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.setblocking (0)
        threading.Thread.__init__ (self)

    @consumer
    def consumeMetric (self, key, data):
        if key not in StatSession_Metrics:
            StatSession_Metrics [key] = []
        if len (StatSession_Metrics [key]) >= self.climit:
            StatSession_Metrics [key] = StatSession_Metrics [key][1:]
        StatSession_Metrics [key].append (data)
    
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
        if which == 'host':
            self.consumeHost (key, data)
        elif which == 'metric':
            self.consumeMetric (key, data)
        elif which == 'log':
            self.consumeLog (key, data)
        else:
            ServerUtil.warning ('Invalid type [%s]' % which)

    def run (self):
        ServerUtil.info ("Starting StatsAggregator on %s:%s" % (self.host, self.port))
        self.serverSocket.bind ((self.host, self.port))
        self.running = True
        inputs = [self.serverSocket]
        try:
            while len (inputs) > 0 and self.running is True:
                (reads, writes, errors) = select.select (
                    inputs, [], inputs, 1
                )
                for i in reads:
                    rdata = i.recvfrom (256)
                    stats = rdata [0].strip ().rstrip ('\0')
                    try:
                        sobject = json.loads (stats)
                        sobject ['host'] = { 'host': rdata [1][0],
                                             'port': rdata [1][1]
                                         }
                        ServerUtil.info ('Recieved [%s] from [%s:%i] for [%s]' \
                                         % (sobject ['type'],
                                            sobject ['host']['host'],
                                            sobject ['host']['port'],
                                            sobject ['name']))
                        self.consume (sobject)
                    except:
                        ServerUtil.debug ("%s" % traceback.format_exc ())
                        ServerUtil.error ("%s" % sys.exc_info ()[1])
        except KeyboardInterrupt:
            ServerUtil.info ("Caught Keyboard interupt closing")
        except:
            ServerUtil.error ("%s" % traceback.format_exc ())
            ServerUtil.error ("%s" % sys.exc_info ()[1])
        finally:
            self.serverSocket.close ()
