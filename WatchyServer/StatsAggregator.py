import sys
import json
import socket
import select
import threading
import traceback
import ServerUtil
from StatsServer import StatSession

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

    def consume (self, data):
        print data
        key = data ['name']
        if key not in StatSession:
            StatSession [key] = []
        if len (StatSession [key]) >= self.climit:
            StatSession [key] = StatSession [key][1:]
        StatSession [key].append (data)
        if self.backend is not None:
            self.backend.consume (key, data)

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
