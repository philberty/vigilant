import os
import sys
import json
import time
import signal
import socket
import asyncio
import syslog
import traceback
import platform
import psutil
import datetime
import daemonize

__STATS_DAEMON_APP = 'watchy'
__STATS_DAEMON_SERVER = None
__STATS_DAEMON_READY = False


def _isDaemonAlive(pid='/tmp/watchy.pid'):
    try:
        with open(pid, 'r') as fd:
            process = fd.read()
            os.kill(int(process), 0)
    except:
        return False
    return True


class ClientDaemonConnection:
    def __init__(self, pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
        self._pid = pid
        self._sock = sock
        self._connect()

    def _connect(self):
        if _isDaemonAlive(self._pid) is False:
            raise Exception('Daemon process not alive [%s]' % self._pid)
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            self._socket.connect(self._sock)
        except:
            raise Exception('Unable to connect to daemon [%s]' % self._sock)

    def close(self):
        self._socket.close()

    def postWatchPid(self, key, pid):
        message = {'type': 'watch', 'key': key, 'pid': pid}
        self._socket.send(json.dumps(message).encode('utf-8'))

    def postStopWatchPid(self, pid):
        message = {'type': 'stopWatchPid', 'pid': pid}
        self._socket.send(json.dumps(message).encode('utf-8'))

    def postStopWatchKey(self, key):
        message = {'type': 'stopWatchKey', 'key': key}
        self._socket.send(json.dumps(message).encode('utf-8'))

    def postLogMessageForKey(self, key, log):
        message = {'type': 'postLog', 'key': key, 'message': log}
        self._socket.send(json.dumps(message).encode('utf-8'))

    def postStopDaemon(self):
        message = {'type': 'stop'}
        self._socket.send(json.dumps(message).encode('utf-8'))


class StatServerDaemon:
    def __init__(self, key, transport, sigpid, pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
        self._transport = transport
        self._sock = sock
        self._sigpid = sigpid
        self._pids = {}
        self._loop = None
        self._key = key
        if _isDaemonAlive(pid):
            raise Exception('Lock [%s] pid is already alive' % pid)

    def _signalParent(self):
        try:
            os.kill(self._sigpid, signal.SIGUSR1)
        except:
            pass

    @asyncio.coroutine
    def _clientConnected(self, reader, _):
        while True:
            data = yield from reader.read(8192)
            if not data:
                break
            try:
                data = json.loads(data.decode('utf-8'))
                syslog.syslog(syslog.LOG_ALERT, "Got message type [%s]!" % data['type'])
            except:
                pass

    @asyncio.coroutine
    def _postHostStats(self):
        while True:
            for key in self._pids:
                pid = self._pids[key]
                process = psutil.Process(pid)
                message = {
                    'key': key,
                    'type': 'pid',
                    'payload': {
                        'pid': pid,
                        'name': process.name(),
                        'user': process.username(),
                        'status': process.status(),
                        'cpu': process.cpu_percent(interval=1.0),
                        'threads': process.threads(),
                        'memory': process.memory_percent(),
                        'io': None,
                        'fds': process.num_fds()
                    }
                }
                self._transport.postMessageOnTransport(json.dumps(message).encode('utf-8'))
            yield from asyncio.sleep(2)

    @asyncio.coroutine
    def _postPidStats(self):
        while True:
            message = {
                'key': self._key,
                'type': 'host',
                'payload':
                    {'platform': platform.platform(),
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
            self._transport.postMessageOnTransport(json.dumps(message).encode('utf-8'))
            yield from asyncio.sleep(4)

    def start(self):
        self._transport.initTransport()
        self._loop = asyncio.new_event_loop()
        asyncio.async(self._postHostStats, loop=self._loop)
        asyncio.async(self._postPidStats, loop=self._loop)
        server = asyncio.start_unix_server(self._clientConnected, path=self._sock, loop=self._loop)
        self._loop.run_until_complete(server)
        self._signalParent()
        try:
            self._loop.run_forever()
        finally:
            self._loop.close()


def _daemonReadyHandler(*args):
    global __STATS_DAEMON_READY
    __STATS_DAEMON_READY = True


def _daemonizeStatsDaemon():
    try:
        __STATS_DAEMON_SERVER.start()
    except:
        syslog.syslog(syslog.LOG_ALERT, str(sys.exc_info()))
        syslog.syslog(syslog.LOG_ALERT, str(traceback.format_exc()))


def forkStatsDaemon(daemon, timeout=3, lock='/tmp/watchy.pid'):
    global __STATS_DAEMON_SERVER, __STATS_DAEMON_READY, __STATS_DAEMON_APP
    __STATS_DAEMON_SERVER = daemon

    signal.signal(signal.SIGUSR1, _daemonReadyHandler)

    pid = os.fork()
    if pid == 0:
        daemon = daemonize.Daemonize(app=__STATS_DAEMON_APP, pid=lock, action=_daemonizeStatsDaemon)
        daemon.start()
        sys.exit(0)

    for i in range(timeout):
        if __STATS_DAEMON_READY is True:
            break
        time.sleep(1)
    if __STATS_DAEMON_READY is False:
        raise Exception('Timeout of [%i] seconds, failed waiting for daemon to come alive' % timeout)
