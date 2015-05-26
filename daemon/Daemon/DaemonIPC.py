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
from . import DaemonState

SYSLOG_DAEMON = '/var/run/syslog' if 'Darwin' in platform() else '/dev/log'


def is_pid_alive(pid: int) -> bool:
    """
    :param pid: the pid to check
    :return: returns true or false if pid is alive
    """
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError as err:
        import errno
        if err.errno == errno.ESRCH:
            return False
    return True


def get_pid_from_lock(lock: str) -> bool:
    """
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


class ClientConnection:
    def __init__(self, pid, sock):
        self._pid = pid
        self._sock = sock
        self._connect()

    def _connect(self):
        if is_pid_alive(get_pid_from_lock(self._pid)) is False:
            raise Exception('Daemon process not alive [%s]' % self._pid)
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            self._socket.connect(self._sock)
            resp = self.post_status_request()
            if resp is None:
                raise Exception('Invalid response from server')
        except:
            raise Exception('Unable to connect to daemon [%s]' % self._sock)

    def _wait_for_response(self, timeout=10) -> dict:
        """
        :param timeout: length of timeout in seconds to wait for response
        :return: dictionary json response or Exception
        """
        inputs = [self._socket]
        reads, _, __ = select.select(inputs, [], [], timeout)
        for i in reads:
            data = i.recv(1024)
            return json.loads(data.decode("utf-8"))
        raise Exception('Failed waiting [%i] seconds for response' % timeout)

    def close(self):
        self._socket.close()

    def post_watch_pid(self, key: str, pid: int):
        """
        Send the daemon a message telling it to monitor the specified process

        :param key: string key to tie a process to could be process name or other
        :param pid: the pid of the process to monitor
        """
        message = {'type': 'watch', 'key': key, 'pid': pid}
        self._socket.sendall(json.dumps(message).encode('utf-8'))

    def post_stop_watch_pid(self, pid: int):
        """
        Send the daemon a message telling it to stop monitoring the specified process

        :param pid: the pid to stop watching
        """
        message = {'type': 'stopWatchPid', 'pid': pid}
        self._socket.sendall(json.dumps(message).encode('utf-8'))

    def post_stop_watch_key(self, key: str):
        """
        Send the daemon a message telling to stop monitoring the process with the specified key

        :param key: the key to stop watching
        """
        message = {'type': 'stopWatchKey', 'key': key}
        self._socket.sendall(json.dumps(message).encode('utf-8'))

    def post_log_message_for_key(self, message: str, proc=DaemonState.STATS_DAEMON_APP):
        """
        Send the daemon a log message to handle against a proc key

        :param message: the string log message
        """
        message = {'type': 'postLog', 'proc': proc, 'message': message}
        self._socket.sendall(json.dumps(message).encode('utf-8'))

    def post_status_request(self) -> dict:
        """
        Send the daemon a message to return the status of it
        :returns: returns json dict response or exception
        """
        self._socket.sendall(json.dumps({'type': 'status'}).encode('utf-8'))
        resp = self._wait_for_response()
        if resp is None:
            raise Exception("Failed waiting for response for status")
        return json.dumps(resp, indent=4)

    def post_stop_daemon(self):
        """
        Send the daemon a message to stop running
        """
        message = {'type': 'stop'}
        self._socket.sendall(json.dumps(message).encode('utf-8'))


def _daemon_ready_handler(*args):
    """
    Wrapper to handle daemon ready signal
    """
    DaemonState.STATS_DAEMON_READY = True


def _daemonize_daemon():
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
        DaemonState.STATS_DAEMON_SERVER.start()


def fork_daemon(daemon, timeout=5, lock='/tmp/vigilant.pid'):
    """
    Fork the stats Daemon as a real system daemon to run in the background

    :param daemon: The StatServerDaemon from StatsAsyncCore
    :param timeout: optional keyword argument for the timeout to wait on daemon ready signal
    :param lock: optional specify the location of the daemon lock file
    :raise Exception: Raises an exception if the timeout elapses before daemon ready
    """
    DaemonState.STATS_DAEMON_SERVER = daemon

    signal.signal(signal.SIGUSR1, _daemon_ready_handler)

    pid = os.fork()
    if pid == 0:
        daemon = daemonize.Daemonize(app=DaemonState.STATS_DAEMON_APP,
                                     pid=lock, action=_daemonize_daemon)
        daemon.start()
        sys.exit(0)

    for i in range(timeout):
        if DaemonState.STATS_DAEMON_READY:
            break
        time.sleep(1)
    if DaemonState.STATS_DAEMON_READY is False:
        raise Exception('Timeout of [%i] seconds, failed waiting for daemon to come alive' % timeout)
