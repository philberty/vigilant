import os
import sys
import json
import time
import socket
import asyncio
import syslog
import traceback
import platform
import psutil
import datetime
import signal
import select
import threading
import daemonize

__STATS_DAEMON_APP = 'watchy'
__STATS_DAEMON_SERVER = None
__STATS_DAEMON_READY = False
__STATS_DAEMON_STOP = False

def isPidAlive(pid):
    if pid <= 0:
        return False
    try:
        os.kill(int(pid), 0)
    except:
        return False
    return True

def getPidFromLockFile(lock='/tmp/watchy.pid'):
    try:
        pid = -1
        with open(lock, 'r') as fd:
            pid = fd.read()
        return int(pid)
    except:
        return pid

def doesFileExist(path):
    try:
        return os.path.isfile(path)
    except:
        return False

class ClientDaemonConnection:
    def __init__(self, pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
        self._pid = pid
        self._sock = sock
        self._connect()

    def _connect(self):
        if isPidAlive(getPidFromLockFile(self._pid)) is False:
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

class StatsServerUnixSocket(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self._sock = sock
        self._running = False
        self.daemon = True
        self._createSocket()

    def _createSocket(self):
        try:
            os.unlink(self._sock)
        except OSError:
            if os.path.exists(self._sock):
                raise
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._socket.setblocking(0)

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        self._running = value

    def _watchyProtocolHandler(self, message):
        global __STATS_DAEMON_STOP
        syslog.syslog(syslog.LOG_ALERT, "Message type [%s]" % message['type'])
        if message['type'] == 'stop':
            __STATS_DAEMON_STOP = True

    def run(self):
        self._running = True
        self._socket.bind(self._sock)
        self._socket.listen(1)
        inputs = [self._socket]
        try:
            while self._running is True:
                (reads, writes, errors) = select.select(
                    inputs, [], inputs
                )
                for i in reads:
                    if i is self._socket:
                        connection, _ = self._socket.accept()
                        connection.setblocking(0)
                        inputs.append(connection)
                    else:
                        try:
                            data = self._socket.recv(1024)
                            if data:
                                message = json.loads(data.decode("utf-8"))
                                self._watchyProtocolHandler(message)
                        except:
                            pass
        except:
            syslog.syslog(syslog.LOG_ALERT, str(sys.exc_info()))
            syslog.syslog(syslog.LOG_ALERT, str(traceback.format_exc()))
        finally:
            self._socket.close()

class StatServerDaemon:
    def __init__(self, key, transport, sigpid, pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
        self._transport = transport
        self._sock = sock
        self._sigpid = sigpid
        self._loop = None
        self._key = key
        self._server = None
        if isPidAlive(getPidFromLockFile(pid)):
            raise Exception('Lock [%s] pid is already alive' % pid)

    def _signalParent(self):
        try:
            os.kill(self._sigpid, signal.SIGUSR1)
        except:
            pass

    def _stopEventLoop(self):
        if self._loop:
            self._loop.stop()
            self._loop.close()
        if self._server:
            self._server.running = False
            if doesFileExist(self._sock):
                os.unlink(self._sock)

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
        global __STATS_DAEMON_STOP
        while True:
            try:
                message = self._getHostStats()
                self._transport.postMessageOnTransport(json.dumps(message).encode('utf-8'))
            except:
                syslog.syslog(syslog.LOG_ALERT, str(sys.exc_info()))
                syslog.syslog(syslog.LOG_ALERT, str(traceback.format_exc()))
            finally:
                yield from asyncio.sleep(4)

    def start(self):
        global __STATS_DAEMON_STOP
        __STATS_DAEMON_STOP = False
        syslog.syslog(syslog.LOG_ALERT, "Starting event loop")
        self._server = StatsServerUnixSocket(self._sock)
        self._transport.initTransport()

        self._loop = asyncio.get_event_loop()
        self._server.start()

        self._signalParent()

        self._loop.run_until_complete(self._postHostStats())
        self._server.running = False
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
