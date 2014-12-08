import os
import sys
import json
import asyncio
import signal
import psutil
import platform
import datetime
import traceback
import syslog

from . import StatsDaemon
from . import StatsDaemonState
from . import StatsDaemonServer

class StatServerDaemon:
    def __init__(self, key, transport, sigpid, pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
        self._transport = transport
        self._sock = sock
        self._sigpid = sigpid
        self._loop = None
        self._key = key
        self._server = None
        self._watching = {}
        if StatsDaemon.isPidAlive(StatsDaemon.getPidFromLockFile(pid)):
            raise Exception('Lock [%s] pid is already alive' % pid)

    def log(self, mess):
        try:
            syslog.syslog(syslog.LOG_ALERT, "%s" % mess)
            message = {'key': self._key + '.StatsDaemon',
                       'type': 'log',
                       'host': self._key,
                       'payload': {'message': mess}
            }
            self._transport.postMessageOnTransport(json.dumps(message).encode('utf-8'))
        except:
            pass

    @property
    def transport(self):
        return self._transport

    @property
    def status(self):
        return self._watching

    @property
    def host(self):
        return self._key

    def watchPid(self, pid, key):
        self.log('Trying to watch pid [%i] for key [%s]' % (pid, key))
        key = self._key + '.' + key
        self._watching[key] = pid

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
                'cpu_stats': psutil.cpu_percent(interval=1, percpu=True),
                'usage': psutil.cpu_times_percent().user,
                'memory_total': psutil.virtual_memory().total,
                'memory_used': psutil.virtual_memory().used,
                'disk_total': psutil.disk_usage('/').total,
                'disk_free': psutil.disk_usage('/').used,
                'timestamp': datetime.datetime.now().isoformat(),
                'processes': len(psutil.pids())
            }
        }

    def _stringifyPsutilStatList(self, data):
        retval = []
        for i in data:
            retval.append(str(i))
        return retval

    def _getStatsForPidWrapper(self, pid):
        p = psutil.Process(pid)
        return {
            'pid': pid,
            'name': p.name(),
            'path': p.exe(),
            'cwd': p.cwd(),
            'cmdline': p.cmdline(),
            'status': p.status(),
            'user': p.username(),
            'threads': p.num_threads(),
            'fds': p.num_fds(),
            'files': self._stringifyPsutilStatList(p.open_files()),
            'usage': p.cpu_percent(interval=1),
            'memory_percent': p.memory_percent(),
            'connections': self._stringifyPsutilStatList(p.connections())
        }

    def _getStatsForPid(self, key, pid):
        try:
            return self._getStatsForPidWrapper(pid)
        except psutil.NoSuchProcess:
            self.log('Process [%i] key [%s] has stopped' % (pid, key))
            del self._watching[key]

    @asyncio.coroutine
    def _postHostStats(self):
        while True:
            try:
                message = self._getHostStats()
                self._transport.postMessageOnTransport(json.dumps(message).encode('utf-8'))
            except:
                self.log(str(sys.exc_info()))
                self.log(str(traceback.format_exc()))
            finally:
                yield from asyncio.sleep(4)

    @asyncio.coroutine
    def _postPidStats(self):
        while True:
            try:
                for key in list(self._watching.keys()):
                    payload = self._getStatsForPid(key, int(self._watching[key]))
                    if payload:
                        message = {'key': key,
                                   'host': self._key,
                                   'type': 'pid', 'payload': payload}
                        self._transport.postMessageOnTransport(json.dumps(message).encode('utf-8'))
            except:
                self.log(str(sys.exc_info()))
                self.log(str(traceback.format_exc()))
            finally:
                yield from asyncio.sleep(4)

    def _runEventLoop(self):
        try:
            self._loop.run_forever()
        except:
            self.log(str(sys.exc_info()))
            self.log(str(traceback.format_exc()))
        finally:
            self._stopEventLoop()

    def start(self):
        self.watchPid(os.getpid(), 'StatsDaemon')
        StatsDaemonState.STATS_DAEMON_TRANSPORT = self._transport
        self._server = StatsDaemonServer.StatsServerUnixSocket(self._sock)
        self._transport.initTransport()
        self._loop = asyncio.get_event_loop()
        self._server.bind()
        self._server.start()
        self._loop.add_signal_handler(signal.SIGTERM, self._stopEventLoop)
        asyncio.async(self._postHostStats(), loop=self._loop)
        asyncio.async(self._postPidStats(), loop=self._loop)
        self._signalParent()
        self._runEventLoop()