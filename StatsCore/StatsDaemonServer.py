import os
import json
import socket
import select
import signal
import logging
import threading

from . import StatsDaemonState


class StatsServerUnixSocket(threading.Thread):
    """
    This could probably be re-written to use asyncio, and eventually will be.
    But directly using select works on Linux and Darwin and it works for now.
    """

    def __init__(self, sock):
        threading.Thread.__init__(self)
        self._sock = sock
        self._running = False
        self.daemon = True
        self._message_queues = {}
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

    def _stopStatsDaemon(self):
        os.kill(os.getpid(), signal.SIGTERM)
        self._running = False

    def _watchPidForKey(self, pid, key):
        StatsDaemonState.STATS_DAEMON_SERVER.watchPid(pid, key)

    def _stopWatchKeyForPid(self, pid):
        pass

    def _stopWatchingPidForKey(self, key):
        pass

    def _postLogMessage(self, payload):
        try:
            message = {'key': StatsDaemonState.STATS_DAEMON_SERVER.host + '.' + payload['key'],
                       'type': 'log',
                       'host': StatsDaemonState.STATS_DAEMON_SERVER.host,
                       'payload': {'message': payload['message']}
            }
            serialized = json.dumps(message).encode('utf-8')
            transport = StatsDaemonState.STATS_DAEMON_SERVER.transport
            transport.postMessageOnTransport(serialized)
        except:
            pass

    def _watchyProtocolHandler(self, message, sock):
        try:
            message_type = message['type']
            logging.info("Message type [%s]" % message_type)
            if message_type == 'stop':
                self._stopStatsDaemon()
            elif message_type == 'status':
                message = StatsDaemonState.STATS_DAEMON_SERVER.status
                sock.send(json.dumps(message).encode('utf-8'))
            elif message_type == 'watch':
                self._watchPidForKey(message['pid'], message['key'])
            elif message_type == 'stopWatchPid':
                self._stopWatchKeyForPid([message['pid']])
            elif message_type == 'stopWatchKey':
                self._stopWatchingPidForKey(message['key'])
            elif message_type == 'postLog':
                self._postLogMessage(message)
            else:
                logging.error("Unhandled message type [%s]" % message_type)
        except:
            logging.error("Failed message dispatch")

    def bind(self):
        self._running = True
        self._socket.bind(self._sock)

    def run(self):
        inputs = [self._socket]
        _timeout = 1
        self._socket.listen(1)
        try:
            while self._running:
                reads, _, errors = select.select(inputs, [], inputs, _timeout)
                for i in reads:
                    if i is self._socket:
                        connection, _ = self._socket.accept()
                        inputs.append(connection)
                    else:
                        data = i.recv(1024)
                        if data:
                            try:
                                message = json.loads(data.decode("utf-8"))
                                self._watchyProtocolHandler(message, i)
                            except:
                                pass
                for i in errors:
                    i.close()
                    inputs.remove(i)
        except:
            pass
        finally:
            self._socket.close()
            os.unlink(self._sock)