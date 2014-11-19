import os
import sys
import json
import syslog
import asyncio
import signal
import psutil
import platform
import datetime
import traceback

from . import StatsDaemon
from . import StatsDaemonServer

STATS_DAEMON_STOP = False

class StatServerDaemon:
    def __init__(self, key, transport, sigpid, pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
        self._transport = transport
        self._sock = sock
        self._sigpid = sigpid
        self._loop = None
        self._key = key
        self._server = None
        if StatsDaemon.isPidAlive(StatsDaemon.getPidFromLockFile(pid)):
            raise Exception('Lock [%s] pid is already alive' % pid)

    def _signalParent(self):
        try:
            os.kill(self._sigpid, signal.SIGUSR1)
        except:
            pass

    def _stopEventLoop(self, *args):
        syslog.syslog(syslog.LOG_ALERT, "holy fuck!")
        if self._server:
            syslog.syslog(syslog.LOG_ALERT, "1")
            self._server.running = False
            syslog.syslog(syslog.LOG_ALERT, "2")
            self._server.join()
            syslog.syslog(syslog.LOG_ALERT, "3")
        if self._loop:
            syslog.syslog(syslog.LOG_ALERT, "4")
            self._loop.stop()
            syslog.syslog(syslog.LOG_ALERT, "5")
            self._loop.close()
            syslog.syslog(syslog.LOG_ALERT, "6")


    def _getHostStats(self):
        return {
            'key': self._key,
            'type': 'host',
            'payload': {
                'platform': platform.platform(),
                'hostname': platform.node(),
                'machine': platform.machine(),
                'version': platform.version(),
                'cores': psutil.cpu_count(),
                'usage': psutil.cpu_times_percent().user,
                'memory_total': psutil.virtual_memory().total,
                'memory_used': psutil.virtual_memory().used,
                'disk_total': psutil.disk_usage('/').total,
                'disk_free': psutil.disk_usage('/').used,
                'timestamp': datetime.datetime.now().isoformat(),
                'process': len(psutil.pids())
            }
        }

    @asyncio.coroutine
    def _postHostStats(self):
        while True:
            if STATS_DAEMON_STOP:
                self._stopEventLoop()
                break
            try:
                message = self._getHostStats()
                self._transport.postMessageOnTransport(json.dumps(message).encode('utf-8'))
            except:
                syslog.syslog(syslog.LOG_ALERT, str(sys.exc_info()))
                syslog.syslog(syslog.LOG_ALERT, str(traceback.format_exc()))
            finally:
                yield from asyncio.sleep(4)
        self._stopEventLoop()

    def start(self):
        global STATS_DAEMON_STOP
        STATS_DAEMON_STOP = False
        self._server = StatsDaemonServer.StatsServerUnixSocket(self._sock)
        self._transport.initTransport()
        self._loop = asyncio.get_event_loop()
        self._server.bind()
        self._signalParent()
        self._server.start()
        self._loop.add_signal_handler(signal.SIGTERM, self._stopEventLoop)
        asyncio.async(self._postHostStats(), loop=self._loop)
        try:
            self._loop.run_forever()
        finally:
            self._stopEventLoop()