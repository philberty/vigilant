import os
import sys
import json
import asyncio
import signal
import psutil
import platform
import datetime
import traceback
import logging

from . import StatsDaemon
from . import StatsDaemonServer

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
        if self._server:
            self._server.running = False
            self._server.join()
            self._server = None
        if self._loop:
            self._loop.stop()
            self._loop.close()
            self._loop = None

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
            try:
                message = self._getHostStats()
                self._transport.postMessageOnTransport(json.dumps(message).encode('utf-8'))
            except:
                logging.error(str(sys.exc_info()))
                logging.error(str(traceback.format_exc()))
            finally:
                yield from asyncio.sleep(4)

    def _runEventLoop(self):
        try:
            self._loop.run_forever()
        except:
            pass
        finally:
            self._stopEventLoop()

    def start(self):
        self._server = StatsDaemonServer.StatsServerUnixSocket(self._sock)
        self._transport.initTransport()
        self._loop = asyncio.get_event_loop()
        self._server.bind()
        self._signalParent()
        self._server.start()
        self._loop.add_signal_handler(signal.SIGTERM, self._stopEventLoop)
        asyncio.async(self._postHostStats(), loop=self._loop)
        self._runEventLoop()