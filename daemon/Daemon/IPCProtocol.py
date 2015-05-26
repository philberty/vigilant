import os
import json
import signal
import asyncio
import logging

from . import DaemonState


class DaemonProtocol(asyncio.Protocol):
    _transport = None

    def connection_made(self, transport):
        self._transport = transport

    @staticmethod
    def _stop_stats_daemon():
        os.kill(os.getpid(), signal.SIGTERM)

    @staticmethod
    def _watch_pid_for_key(pid, key):
        DaemonState.STATS_DAEMON_SERVER.watch_pid(pid, key)

    def _stop_watch_key_for_pid(self, pid):
        pass

    def _stop_watching_pid_for_key(self, key):
        pass

    def _post_log_message(self, payload):
        message = {'type': payload['proc'],
                    'key': 'internal',
                    'host': DaemonState.STATS_DAEMON_SERVER.host,
                    'payload': {'message': payload['message']}
                }
        transport = DaemonState.STATS_DAEMON_SERVER.transport
        transport.post_message_on_transport(message)

    def _protocol_handler(self, message):
        message_type = message['type']
        logging.info("Message type [%s]" % message_type)
        if message_type == 'stop':
            self._stop_stats_daemon()
        elif message_type == 'status':
            message = DaemonState.STATS_DAEMON_SERVER.status
            self._transport.write(json.dumps(message).encode('utf-8'))
        elif message_type == 'watch':
            self._watch_pid_for_key(message['pid'], message['key'])
        elif message_type == 'stopWatchPid':
            self._stop_watch_key_for_pid([message['pid']])
        elif message_type == 'stopWatchKey':
            self._stop_watching_pid_for_key(message['key'])
        elif message_type == 'postLog':
            self._post_log_message(message)
        else:
            logging.error("Unhandled message type [%s]" % message_type)

    def data_received(self, data):
        try:
            message = json.loads(data.decode("utf-8"))
            self._protocol_handler(message)
        except:
            logging.error("Failed message dispatch")

    def connection_lost(self, exc):
        self._transport.close()
