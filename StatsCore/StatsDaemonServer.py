import os
import json
import socket
import select
import syslog
import threading

from . import StatsDaemonState

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
        syslog.syslog(syslog.LOG_ALERT, "Message type [%s]" % message['type'])
        if message['type'] == 'stop':
            StatsDaemonState.STATS_DAEMON_STOP = True

    def bind(self):
        self._running = True
        self._socket.bind(self._sock)

    def run(self):
        inputs = [self._socket]
        self._socket.listen(1)
        try:
            while self._running:
                (reads, writes, errors) = select.select(
                    inputs, [], inputs, 1
                )
                for i in reads:
                    if i is self._socket:
                        connection, _ = self._socket.accept()
                        connection.setblocking(0)
                        inputs.append(connection)
                    else:
                        data = i.recv(1024)
                        if data:
                            try:
                                message = json.loads(data.decode("utf-8"))
                                self._watchyProtocolHandler(message)
                            except:
                                pass
                        else:
                            i.close()
                            inputs.remove(i)
                for i in errors:
                    i.close()
                    inputs.remove(i)
        except:
            pass
        finally:
            self._socket.close()
            os.unlink(self._sock)