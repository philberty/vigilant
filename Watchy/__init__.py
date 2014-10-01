from . import App
from . import StatsServer


class DashboardApp:
    def __init__(self, host="localhost", port=8080):
        pass


class StatsServer:
    def __init__(self, host="localhost", port=8081):
        self._server = StatsServer.UDPStatsServer(host, port)

   def stop(self):
       self._server.running = False

    def listen(self, blocking=False):
        if blocking is False:
            self._server.run()
        else:
            self._server.start()
