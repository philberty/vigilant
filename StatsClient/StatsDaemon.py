import os
import sys
import json
import time
import socket
import syslog
import traceback
import signal
import daemonize

__STATS_DAEMON_APP = 'watchy'
__STATS_DAEMON_SERVER = None
__STATS_DAEMON_READY = False

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
