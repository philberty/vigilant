import os
import sys
import asyncio
import signal
import psutil
import traceback
import syslog

from . import DaemonIPC
from . import DaemonState
from . import IPCProtocol
from . import StatsMonitor

from urllib.parse import quote as urlencode


class StatsDaemon:
    def __init__(self, key, transport, sigpid, pid, sock):
        self._transport = transport
        self._sock = sock
        self._sigpid = sigpid
        self._loop = None
        self._key = urlencode(key)
        self._watching = {}
        if DaemonIPC.is_pid_alive(DaemonIPC.get_pid_from_lock(pid)):
            raise Exception('Lock [%s] pid is already alive' % pid)

    @property
    def transport(self):
        return self._transport

    @property
    def host(self):
        return self._key

    @property
    def status(self):
        return {
            'host': self.host,
            'transport': self.transport.status(),
            'watching': self._watching
        }

    def log(self, mess, proc=DaemonState.STATS_DAEMON_APP):
        syslog.syslog(syslog.LOG_ALERT, "%s: %s" % (proc, mess))
        message = {'key': proc,
                   'type': 'log',
                   'host': self.host,
                   'payload': {'message': mess}
                }
        self.transport.post_message_on_transport(message)

    def watch_pid(self, pid, key):
        self._watching[urlencode(key)] = pid
        self.log('Watching pid [%i] for key [%s]' % (pid, key))

    @asyncio.coroutine
    def signal_parent_ready(self):
        os.kill(self._sigpid, signal.SIGUSR1)

    def stop_event_loop(self, *args):
        self._loop.stop()

    def get_stats_for_pid(self, key, pid):
        try:
            return StatsMonitor.get_stats_for_pid(pid)
        except psutil.NoSuchProcess:
            self.log('Process [%i] key [%s] has stopped' % (pid, key))
            del self._watching[key]

    @asyncio.coroutine
    def post_host_stats(self):
        while True:
            try:
                message = StatsMonitor.get_host_stats(self.host)
                self.transport.post_message_on_transport(message)
            except:
                self.log(str(sys.exc_info()))
                self.log(str(traceback.format_exc()))
            finally:
                yield from asyncio.sleep(3)

    @asyncio.coroutine
    def post_pid_stats(self):
        while True:
            try:
                for key in list(self._watching.keys()):
                    payload = self.get_stats_for_pid(key, int(self._watching[key]))
                    if payload:
                        message = {'key': key,
                                   'host': self.host,
                                   'type': 'pid',
                                   'payload': payload}
                        self.transport.post_message_on_transport(message)
            except:
                self.log(str(sys.exc_info()))
                self.log(str(traceback.format_exc()))
            finally:
                yield from asyncio.sleep(3)

    def run_event_loop(self):
        self.log('Daemon ready...')
        try:
            self._loop.run_forever()
        finally:
            self._loop.close()

    def start_transport(self):
        self._transport.init_transport()
        DaemonState.STATS_DAEMON_TRANSPORT = self._transport

    def create_io_loop(self):
        self._loop = asyncio.get_event_loop()
        self._loop.add_signal_handler(signal.SIGTERM, self.stop_event_loop)

    def unlink_previous_socket(self):
        try:
            os.unlink(self._sock)
        except:
            pass

    def create_ipc_server(self):
        self.unlink_previous_socket()
        server = self._loop.create_unix_server(IPCProtocol.DaemonProtocol, path=self._sock)
        asyncio.async(server, loop=self._loop)
        asyncio.async(self.signal_parent_ready(), loop=self._loop)

    def create_monitor_routines(self):
        asyncio.async(self.post_host_stats(), loop=self._loop)
        asyncio.async(self.post_pid_stats(), loop=self._loop)

    def start(self):
        self.start_transport()
        self.create_io_loop()
        self.create_ipc_server()
        self.create_monitor_routines()
        self.watch_pid(os.getpid(), DaemonState.STATS_DAEMON_APP)
        self.run_event_loop()
