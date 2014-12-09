import os
import sys
import json
import time
import socket
import signal
import select
import daemonize
import traceback

import syslog
import logging
import logging.handlers

from platform import platform
from . import StatsDaemonState

SYSLOG_DAEMON = '/var/run/syslog' if 'Darwin' in platform() else '/dev/log'

# Please someone get rid of these functions for me!!!
# :'( they are so disgusting
def isPidAlive(pid):
    if pid <= 0:
        return False
    try:
        os.kill(int(pid), 0)
    except:
        return False
    return True

def getPidFromLockFile(lock='/tmp/watchy.pid'):
    """
    Returns the pid inside the specified lock file else returns -1

    :param lock: the lock file to open and read for the pid
    :return: returns the pid inside the specified lock file else -1
    """
    try:
        pid = -1
        with open(lock, 'r') as fd:
            pid = fd.read()
        return int(pid)
    except:
        return pid

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

    def _waitForJsonResponse(self, timeout=5):
        inputs = [self._socket]
        reads, _, __ = select.select(inputs, [], [], timeout)
        for i in reads:
            data = i.recv(1024)
            return json.loads(data.decode("utf-8"))

    def close(self):
        self._socket.close()

    def postWatchPid(self, key, pid):
        """
        Send the daemon a message telling it to monitor the specified process

        :param key: string key to tie a process to could be process name or other
        :param pid: the pid of the process to monitor
        """
        message = {'type': 'watch', 'key': key, 'pid': pid}
        self._socket.send(json.dumps(message).encode('utf-8'))

    def postStopWatchPid(self, pid):
        """
        Send the daemon a message telling it to stop monitoring the specified process

        :param pid: the pid to stop watching
        """
        message = {'type': 'stopWatchPid', 'pid': pid}
        self._socket.send(json.dumps(message).encode('utf-8'))

    def postStopWatchKey(self, key):
        """
        Send the daemon a message telling to stop monitoring the process with the specified key

        :param key: the key to stop watching
        """
        message = {'type': 'stopWatchKey', 'key': key}
        self._socket.send(json.dumps(message).encode('utf-8'))

    def postLogMessageForKey(self, key, log):
        """
        Send the daemon a log message to handle against a key

        :param key: key to post log message against
        :param log: the string log message
        """
        message = {'type': 'postLog', 'key': key, 'message': log}
        self._socket.send(json.dumps(message).encode('utf-8'))

    def postDaemonStatusMessage(self):
        """
        Send the daemon a message to return the status of it
        """
        self._socket.send(json.dumps({'type': 'status'}).encode('utf-8'))
        try:
            resp = self._waitForJsonResponse()
            return json.dumps(resp, indent=4)
        except:
            return None

    def postStopDaemon(self):
        """
        Send the daemon a message to stop running
        """
        message = {'type': 'stop'}
        self._socket.send(json.dumps(message).encode('utf-8'))


def _daemonReadyHandler(*args):
    """
    Wrapper to handle daemon ready signal
    """
    StatsDaemonState.STATS_DAEMON_READY = True


def _daemonizeStatsDaemon():
    """
    Wrapper to handle the daemonization
    """
    try:
        my_logger = logging.getLogger('root')
        my_logger.setLevel(logging.INFO)
        handler = logging.handlers.SysLogHandler(address=SYSLOG_DAEMON)
        my_logger.addHandler(handler)
    except:
        syslog.syslog(syslog.LOG_ALERT, 'Unable to setup logging [%s]' % str(sys.exc_info()[1]))
        syslog.syslog(syslog.LOG_ALERT, '%s' % str(traceback.format_exc()))
    finally:
        StatsDaemonState.STATS_DAEMON_SERVER.start()


def forkStatsDaemon(daemon, timeout=3, lock='/tmp/watchy.pid'):
    """
    Fork the stats Daemon as a real system daemon to run in the background

    :param daemon: The StatServerDaemon from StatsAsyncCore
    :param timeout: optional keyword argument for the timeout to wait on daemon ready signal
    :param lock: optional specify the location of the daemon lock file
    :raise Exception: Raises an exception if the timeout elapses before daemon ready
    """
    StatsDaemonState.STATS_DAEMON_SERVER = daemon

    signal.signal(signal.SIGUSR1, _daemonReadyHandler)

    pid = os.fork()
    if pid == 0:
        daemon = daemonize.Daemonize(app=StatsDaemonState.STATS_DAEMON_APP,
                                     pid=lock, action=_daemonizeStatsDaemon)
        daemon.start()
        sys.exit(0)

    for i in range(timeout):
        if StatsDaemonState.STATS_DAEMON_READY:
            break
        time.sleep(1)
    if StatsDaemonState.STATS_DAEMON_READY is False:
        raise Exception('Timeout of [%i] seconds, failed waiting for daemon to come alive' % timeout)
