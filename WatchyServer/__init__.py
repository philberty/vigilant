import sys
import traceback
import ServerUtil

from StatsApp import app
from gevent.pywsgi import WSGIServer
from StatsAggregator import UDPStatsServer

class WatchyDServer:
    def __init__ (self, cacheLimit, backends, wbind='localhost', wport=8080,
                  ubind='localhost', uport=8081):
        self.web_bind = wbind
        self.web_port = wport
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
            self.udp_server.running = Falseo

