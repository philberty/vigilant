import sys
import json
import socket
import select
import threading
import traceback
import ServerUtil

from StatsServer import StatSession_Hosts
from StatsServer import StatSession_Metrics

def consume (func):
    def decorated (*args, **kwargs):
        if hasattr (args [0], 'backend'):
            # TODO consume to backend
            pass
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

    @consume
    def consumeMetric (self, key, data):
        if key not in StatSession_Metrics:
            StatSession_Metrics [key] = []
        if len (StatSession_Metrics [key]) >= self.climit:
            StatSession_Metrics [key] = StatSession_Metrics [key][1:]
        StatSession_Metrics [key].append (data)
    
    @consume
    def consumeHost (self, key, data):
        if key not in StatSession_Hosts:
            StatSession_Hosts [key] = []
        if len (StatSession_Hosts [key]) >= self.climit:
            StatSession_Hosts [key] = StatSession_Hosts [key][1:]
        StatSession_Hosts [key].append (data)

    def consume (self, data):
        try:
            key = data ['name']
            which = data ['type']
            if which == 'host':
                self.consumeHost (key, data)
            elif which == 'metric':
                self.consumeMetric (key, data)
            else:
                ServerUtil.warning ('Invalid type [%s]' % which)
        except:
            pass

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
                        ServerUtil.info ('Recieved stats from [%s:%i] for [%s]' \
                                         % (sobject ['host']['host'],
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
